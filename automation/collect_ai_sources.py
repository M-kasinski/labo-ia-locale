#!/usr/bin/env python3
"""Collect structured AI signals for the Labo IA editorial cron.

No X/Twitter scraping, no authenticated social account. The collector uses
first-party feeds/APIs and writes a small shortlist for the publishing agent.
"""

from __future__ import annotations

import argparse
import email.utils
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict, replace
from datetime import datetime, timezone, timedelta
from html import unescape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = ROOT / "automation"
SOURCES_PATH = AUTOMATION_DIR / "sources.json"
STATE_PATH = AUTOMATION_DIR / "source_state.json"
LATEST_PATH = AUTOMATION_DIR / "latest_signals.json"
RUNS_DIR = AUTOMATION_DIR / "runs"
USER_AGENT = "LaboIA-SourceRadar/0.1 (+https://labo-ia-locale.vercel.app)"
TIMEOUT_SECONDS = 20

LOCAL_KEYWORDS = {
    "llama.cpp", "ollama", "mlx", "gguf", "vllm", "inference", "local", "quant",
    "quantization", "apple silicon", "cuda", "rocm", "metal", "runtime", "serving",
    "open-weight", "open weight", "weights", "safetensors", "onnx", "tensorrt",
}
FRONTIER_KEYWORDS = {
    "openai", "anthropic", "claude", "gemini", "mistral", "deepseek", "qwen",
    "llama", "grok", "frontier", "benchmark", "reasoning", "multimodal", "agent",
}


@dataclass
class Signal:
    title: str
    url: str
    source: str
    source_type: str
    published_at: str
    category: str
    score: int
    authority: int
    why_relevant: str
    needs_web_verification: bool
    tags: list[str]
    seen_before: bool = False
    editorial_decision: str = "unreviewed"
    editorial_reason: str = ""


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    raw = value.strip()
    if not raw:
        return None
    # Atom / ISO
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass
    # RSS / RFC2822
    try:
        dt = email.utils.parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def fetch_text(url: str, *, timeout: int = TIMEOUT_SECONDS) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/json, text/xml, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


def fetch_json(url: str) -> Any:
    return json.loads(fetch_text(url))


def clean_text(value: str | None, limit: int = 260) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def load_sources() -> dict[str, Any]:
    return json.loads(SOURCES_PATH.read_text(encoding="utf-8"))


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"seen_urls": {}}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"seen_urls": {}}


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize_url(url: str) -> str:
    return url.strip()


def fingerprint(url: str, title: str) -> str:
    return hashlib.sha256(f"{url}\n{title}".encode("utf-8")).hexdigest()[:16]


def score_signal(title: str, summary: str, source_type: str, authority: int, published_at: datetime | None, base_category: str, seen_before: bool, tags: list[str]) -> tuple[int, str, str, bool]:
    text = f"{title} {summary} {' '.join(tags)}".lower()
    score = 0
    reasons: list[str] = []

    if source_type in {"rss", "github_release"}:
        score += 45
        reasons.append("source primaire structurée")
    if source_type == "github_release":
        score += 15
        reasons.append("release GitHub officielle")
    if source_type == "huggingface_model_created":
        score += 40
        reasons.append("nouveau modèle Hugging Face")
    if source_type == "huggingface_model_modified":
        score += 25
        reasons.append("modèle Hugging Face récemment modifié")
    if source_type == "arxiv_paper":
        score += 30
        reasons.append("papier arXiv récent")

    score += min(35, max(0, authority - 60) // 2)

    local_hits = [kw for kw in LOCAL_KEYWORDS if kw in text]
    frontier_hits = [kw for kw in FRONTIER_KEYWORDS if kw in text]
    if local_hits:
        score += 20
        reasons.append("impact local AI probable: " + ", ".join(local_hits[:3]))
    elif frontier_hits:
        score += 10
        reasons.append("actualité IA générale: " + ", ".join(frontier_hits[:3]))

    if any(word in text for word in ["release", "changelog", "tag", "version", "weights", "model"]):
        score += 10
        reasons.append("artefact concret détecté")

    needs_web_verification = source_type in {"arxiv_paper", "huggingface_model_modified"}
    if needs_web_verification:
        reasons.append("à vérifier avant article long")

    if published_at is None:
        score -= 30
        reasons.append("date ambiguë")
    else:
        age = now_utc() - published_at
        if age > timedelta(days=3):
            score -= 60
            reasons.append("hors fenêtre de fraîcheur 3 jours")
        elif age <= timedelta(days=1):
            score += 10
            reasons.append("très frais")

    if seen_before:
        score -= 50
        reasons.append("déjà vu")

    category = base_category
    if category == "veille" and local_hits:
        category = "local"
    if source_type == "arxiv_paper" and score < 75:
        category = "radar"

    return max(0, score), category, "; ".join(reasons[:5]), needs_web_verification


def parse_feed_entries(xml_text: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml_text)
    entries: list[dict[str, str]] = []
    ns_atom = "{http://www.w3.org/2005/Atom}"

    if root.tag.endswith("rss") or root.find("channel") is not None:
        channel = root.find("channel")
        for item in (channel.findall("item") if channel is not None else []):
            link = clean_text(item.findtext("link"), 500)
            entries.append({
                "title": clean_text(item.findtext("title"), 500),
                "url": link,
                "published_at": clean_text(item.findtext("pubDate") or item.findtext("date"), 120),
                "summary": clean_text(item.findtext("description"), 600),
            })
        return entries

    for entry in root.findall(f"{ns_atom}entry"):
        link = ""
        for link_el in entry.findall(f"{ns_atom}link"):
            href = link_el.attrib.get("href", "")
            rel = link_el.attrib.get("rel", "alternate")
            if href and rel in {"alternate", ""}:
                link = href
                break
        if not link:
            id_el = entry.findtext(f"{ns_atom}id")
            link = id_el or ""
        entries.append({
            "title": clean_text(entry.findtext(f"{ns_atom}title"), 500),
            "url": link,
            "published_at": clean_text(entry.findtext(f"{ns_atom}updated") or entry.findtext(f"{ns_atom}published"), 120),
            "summary": clean_text(entry.findtext(f"{ns_atom}summary") or entry.findtext(f"{ns_atom}content"), 600),
        })
    return entries


def collect_feed(source: dict[str, Any], source_type: str, state: dict[str, Any], limit: int = 8) -> list[Signal]:
    xml_text = fetch_text(source["url"])
    entries = parse_feed_entries(xml_text)[:limit]
    signals: list[Signal] = []
    for item in entries:
        url = normalize_url(item["url"])
        if not url:
            continue
        published = parse_datetime(item.get("published_at"))
        seen = url in state.get("seen_urls", {})
        authority = int(source.get("authority", 75))
        tags = list(source.get("tags", []))
        score, category, why, needs = score_signal(item["title"], item.get("summary", ""), source_type, authority, published, source.get("category", "veille"), seen, tags)
        signals.append(Signal(
            title=item["title"],
            url=url,
            source=source["name"],
            source_type=source_type,
            published_at=(published or now_utc()).isoformat(),
            category=category,
            score=score,
            authority=authority,
            why_relevant=why,
            needs_web_verification=needs,
            tags=tags,
            seen_before=seen,
        ))
    return signals


def collect_huggingface(sources: dict[str, Any], state: dict[str, Any]) -> list[Signal]:
    cfg = sources.get("huggingface", {})
    orgs = {org.lower() for org in cfg.get("orgs", [])}
    endpoints = [
        ("huggingface_model_created", cfg.get("text_generation_created"), 88),
        ("huggingface_model_modified", cfg.get("text_generation_modified"), 78),
    ]
    signals: list[Signal] = []
    for source_type, url, authority in endpoints:
        if not url:
            continue
        models = fetch_json(url)
        if not isinstance(models, list):
            continue
        for model in models[:50]:
            model_id = str(model.get("id") or "").strip()
            if not model_id or "/" not in model_id:
                continue
            org = model_id.split("/", 1)[0].lower()
            tags = [str(t) for t in model.get("tags") or []]
            # MVP 1.5: keep Hugging Face as a reliable source by restricting
            # candidates to watched organisations. Random user fine-tunes are useful
            # for discovery, but too noisy for autonomous article selection.
            if org not in orgs:
                continue
            url_model = f"https://huggingface.co/{model_id}"
            published = parse_datetime(model.get("createdAt") if source_type.endswith("created") else model.get("lastModified"))
            seen = url_model in state.get("seen_urls", {})
            title = f"Hugging Face: {model_id}"
            score, category, why, needs = score_signal(title, str(model.get("pipeline_tag") or ""), source_type, authority, published, "local", seen, tags)
            signals.append(Signal(
                title=title,
                url=url_model,
                source="Hugging Face Hub",
                source_type=source_type,
                published_at=(published or now_utc()).isoformat(),
                category=category,
                score=score,
                authority=authority,
                why_relevant=why,
                needs_web_verification=needs,
                tags=tags[:12],
                seen_before=seen,
            ))
    return signals


def collect_arxiv(sources: dict[str, Any], state: dict[str, Any]) -> list[Signal]:
    cfg = sources.get("arxiv", {})
    signals: list[Signal] = []
    for category_name in cfg.get("categories", []):
        params = urllib.parse.urlencode({
            "search_query": f"cat:{category_name}",
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": int(cfg.get("max_results_per_category", 10)),
        })
        url = f"https://export.arxiv.org/api/query?{params}"
        try:
            xml_text = fetch_text(url, timeout=30)
        except Exception:
            # arXiv is occasionally slow; fail soft so one source does not kill the run.
            continue
        for item in parse_feed_entries(xml_text)[: int(cfg.get("max_results_per_category", 10))]:
            paper_url = normalize_url(item["url"])
            if not paper_url:
                continue
            published = parse_datetime(item.get("published_at"))
            seen = paper_url in state.get("seen_urls", {})
            tags = [category_name, "arxiv"]
            score, out_category, why, needs = score_signal(item["title"], item.get("summary", ""), "arxiv_paper", 70, published, "radar", seen, tags)
            signals.append(Signal(
                title=item["title"],
                url=paper_url,
                source=f"arXiv {category_name}",
                source_type="arxiv_paper",
                published_at=(published or now_utc()).isoformat(),
                category=out_category,
                score=score,
                authority=70,
                why_relevant=why,
                needs_web_verification=needs,
                tags=tags,
                seen_before=seen,
            ))
        time.sleep(1.0)  # polite arXiv access
    return signals


def dedupe(signals: list[Signal]) -> list[Signal]:
    by_key: dict[str, Signal] = {}
    for signal in signals:
        key = signal.url or fingerprint(signal.url, signal.title)
        previous = by_key.get(key)
        if previous is None or signal.score > previous.score:
            by_key[key] = signal
    return sorted(by_key.values(), key=lambda s: (s.score, s.published_at), reverse=True)


VERSION_ONLY_RE = re.compile(r"^(?:v?\d+(?:\.\d+){1,3}(?:[-+][a-z0-9.]+)?|b\d{3,6})$", re.IGNORECASE)
SUBSTANTIVE_TERMS = {
    "agent", "agents", "apple", "silicon", "mlx", "cuda", "rocm", "metal", "vulkan",
    "gguf", "kv", "cache", "performance", "perf", "speed", "latency", "throughput",
    "server", "serving", "batch", "batched", "inference", "reasoning", "speculative",
    "quant", "quantization", "security", "privacy", "memory", "context", "multimodal",
    "weights", "open-weight", "benchmark", "tool", "mcp", "runtime", "local",
}
STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "sur", "pour", "avec", "dans", "une",
    "des", "les", "aux", "du", "de", "la", "le", "un", "ia", "ai", "llm", "release",
    "releases", "version", "model", "models", "github", "hugging", "face",
}


def tokenize_topic(text: str) -> set[str]:
    tokens = {token.lower() for token in re.findall(r"[a-zA-Z0-9]+", text)}
    normalized = set(tokens)
    if "llama" in tokens and "cpp" in tokens:
        normalized.add("llama.cpp")
    return {token for token in normalized if len(token) >= 3 and token not in STOPWORDS}


def load_existing_article_topics(blog_dir: Path | None = None) -> set[str]:
    blog_dir = blog_dir or ROOT / "src" / "content" / "blog"
    topics: set[str] = set()
    if not blog_dir.exists():
        return topics
    for path in blog_dir.glob("*.md*"):
        topics.update(tokenize_topic(path.stem.replace("-", " ")))
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")[:1200]
        except Exception:
            continue
        for field in ("title", "description"):
            match = re.search(rf"^{field}:\s*[\"']?(.*?)[\"']?\s*$", text, flags=re.MULTILINE)
            if match:
                topics.update(tokenize_topic(match.group(1)))
    return topics


def is_version_only_release(signal: Signal) -> bool:
    return signal.source_type == "github_release" and bool(VERSION_ONLY_RE.match(signal.title.strip()))


def has_substantive_signal(signal: Signal) -> bool:
    text = f"{signal.title} {signal.why_relevant}".lower()
    return any(term in text for term in SUBSTANTIVE_TERMS)


def is_likely_duplicate(signal: Signal, existing_topics: set[str]) -> bool:
    if not existing_topics:
        return False
    tokens = tokenize_topic(f"{signal.title} {signal.source} {' '.join(signal.tags)}")
    overlap = tokens & existing_topics
    if len(existing_topics) <= 25:
        return len(overlap) >= 3 or bool({"llama.cpp", "ollama", "vllm", "mlx"}.intersection(overlap) and len(overlap) >= 2)
    # The real article corpus has hundreds of broad tokens. Avoid treating generic
    # words like "openai" or "inference" as duplicates unless a fuller topic matches.
    return len(overlap) >= 5


def apply_editorial_review(
    signals: list[Signal],
    *,
    existing_topics: set[str],
    article_threshold: int = 75,
    radar_threshold: int = 50,
) -> list[Signal]:
    reviewed: list[Signal] = []
    for signal in signals:
        score = signal.score
        decision = "ignore"
        reason = "below editorial threshold"

        if is_version_only_release(signal):
            score = min(score, article_threshold - 1)
            reason = "version-only release without substantive signal"
        elif is_likely_duplicate(signal, existing_topics):
            score = min(score, radar_threshold - 1)
            reason = "likely duplicate of existing article topic"
        elif signal.seen_before:
            score = min(score, radar_threshold - 1)
            reason = "already seen in source state"
        elif score >= article_threshold and not signal.needs_web_verification:
            decision = "article_candidate"
            reason = "passes source, freshness and substance checks"
        elif score >= radar_threshold:
            decision = "radar_candidate"
            reason = "interesting but requires verification or is below article bar"

        reviewed.append(replace(signal, score=max(0, score), editorial_decision=decision, editorial_reason=reason))
    priority = {"article_candidate": 0, "radar_candidate": 1, "ignore": 2}
    return sorted(reviewed, key=lambda s: (priority.get(s.editorial_decision, 3), -s.score, s.published_at))


def build_shortlists(signals: list[Signal], *, max_articles: int = 5, max_radar: int = 10) -> dict[str, list[dict[str, Any]]]:
    article_candidates = [s for s in signals if s.editorial_decision == "article_candidate"][:max_articles]
    radar_candidates = [s for s in signals if s.editorial_decision == "radar_candidate"][:max_radar]
    return {
        "top_article_candidates": [asdict(s) for s in article_candidates],
        "top_radar_candidates": [asdict(s) for s in radar_candidates],
    }


def collect_all(*, update_state: bool) -> dict[str, Any]:
    sources = load_sources()
    state = load_state()
    errors: list[dict[str, str]] = []
    signals: list[Signal] = []

    for source in sources.get("rss", []):
        try:
            signals.extend(collect_feed(source, "rss", state))
        except Exception as exc:
            errors.append({"source": source.get("name", "rss"), "error": f"{type(exc).__name__}: {exc}"})

    for source in sources.get("github_releases", []):
        try:
            signals.extend(collect_feed(source, "github_release", state))
        except Exception as exc:
            errors.append({"source": source.get("name", "github"), "error": f"{type(exc).__name__}: {exc}"})

    try:
        signals.extend(collect_huggingface(sources, state))
    except Exception as exc:
        errors.append({"source": "Hugging Face Hub", "error": f"{type(exc).__name__}: {exc}"})

    try:
        signals.extend(collect_arxiv(sources, state))
    except Exception as exc:
        errors.append({"source": "arXiv", "error": f"{type(exc).__name__}: {exc}"})

    ranked = dedupe(signals)
    article_threshold = int(sources.get("scoring", {}).get("article_threshold", 75))
    radar_threshold = int(sources.get("scoring", {}).get("radar_threshold", 50))
    reviewed = apply_editorial_review(
        ranked,
        existing_topics=load_existing_article_topics(),
        article_threshold=article_threshold,
        radar_threshold=radar_threshold,
    )
    shortlists = build_shortlists(reviewed, max_articles=5, max_radar=10)
    payload = {
        "generated_at": now_utc().isoformat(),
        "policy": {
            "x_search": "disabled / not used",
            "article_threshold": article_threshold,
            "radar_threshold": radar_threshold,
            "max_age_days": int(sources.get("scoring", {}).get("max_age_days", 3)),
        },
        "summary": {
            "total_signals": len(reviewed),
            "article_candidates": sum(1 for s in reviewed if s.editorial_decision == "article_candidate"),
            "radar_candidates": sum(1 for s in reviewed if s.editorial_decision == "radar_candidate"),
            "ignored": sum(1 for s in reviewed if s.editorial_decision == "ignore"),
            "errors": len(errors),
        },
        **shortlists,
        "signals": [asdict(s) for s in reviewed[:80]],
        "errors": errors,
    }

    AUTOMATION_DIR.mkdir(exist_ok=True)
    RUNS_DIR.mkdir(exist_ok=True)
    LATEST_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    run_path = RUNS_DIR / f"{now_utc().strftime('%Y%m%dT%H%M%SZ')}.json"
    run_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if update_state:
        seen_urls = state.setdefault("seen_urls", {})
        for signal in reviewed:
            seen_urls.setdefault(signal.url, {
                "first_seen": payload["generated_at"],
                "status": "seen",
                "source": signal.source,
                "title": signal.title,
                "score": signal.score,
            })
        save_state(state)

    return payload


def check_sources() -> int:
    sources = load_sources()
    checks: list[tuple[str, str]] = []
    for source in sources.get("rss", []):
        checks.append((source["name"], source["url"]))
    for source in sources.get("github_releases", []):
        checks.append((source["name"], source["url"]))
    hf = sources.get("huggingface", {})
    for key in ["text_generation_created", "text_generation_modified"]:
        checks.append((f"Hugging Face {key}", hf[key]))
    # One arXiv category as a smoke test; full collector handles arXiv failures softly.
    cat = sources.get("arxiv", {}).get("categories", ["cs.CL"])[0]
    checks.append((f"arXiv {cat}", "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({
        "search_query": f"cat:{cat}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": 1,
    })))

    failed = 0
    for name, url in checks:
        try:
            text = fetch_text(url, timeout=30)
            print(f"OK   {name}: {len(text)} bytes")
        except Exception as exc:
            failed += 1
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect AI source signals for Labo IA")
    parser.add_argument("--check-sources", action="store_true", help="Fetch each configured source once and print OK/FAIL")
    parser.add_argument("--update-state", action="store_true", help="Mark current URLs as seen after collection")
    args = parser.parse_args()

    if args.check_sources:
        return check_sources()

    payload = collect_all(update_state=args.update_state)
    print(json.dumps(payload["summary"], indent=2, ensure_ascii=False))
    if payload.get("errors"):
        print("Errors:", json.dumps(payload["errors"], indent=2, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
