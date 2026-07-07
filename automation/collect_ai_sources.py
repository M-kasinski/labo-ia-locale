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
import subprocess
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
EDITORIAL_PREVIEW_PATH = AUTOMATION_DIR / "editorial_preview.md"
RUN_REPORT_PATH = AUTOMATION_DIR / "run_report.md"
DEBUG_PAYLOAD_PATH = AUTOMATION_DIR / "radar_debug.json"
RUNS_DIR = AUTOMATION_DIR / "runs"
USER_AGENT = "LaboIA-SourceRadar/0.1 (+https://labo-ia-locale.vercel.app)"
TIMEOUT_SECONDS = 20
HTML_WATCHER_TIMEOUT_SECONDS = 8

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
    result = subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--max-time",
            str(timeout),
            "-A",
            USER_AGENT,
            "-H",
            "Accept: application/rss+xml, application/atom+xml, application/json, text/xml, */*",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=timeout + 2,
    )
    if result.returncode != 0:
        error = clean_text(result.stderr, 500) or f"curl exited with {result.returncode}"
        raise RuntimeError(f"fetch failed for {url}: {error}")
    return result.stdout


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
        return {"seen_urls": {}, "signals": {}}
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        state.setdefault("seen_urls", {})
        state.setdefault("signals", {})
        return state
    except Exception:
        return {"seen_urls": {}, "signals": {}}


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize_url(url: str) -> str:
    return url.strip()


def normalize_title(title: str) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", title.lower())
    return re.sub(r"\s+", " ", text).strip()


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
            xml_text = fetch_text(url, timeout=int(cfg.get("timeout_seconds", 12)))
        except Exception:
            # arXiv is occasionally slow; fail soft so one source does not kill the run.
            continue
        for item in parse_feed_entries(xml_text)[: int(cfg.get("max_results_per_category", 10))]:
            paper_url = normalize_url(item["url"])
            if not paper_url:
                continue
            published = parse_datetime(item.get("published_at"))
            seen = paper_url in state.get("seen_urls", {}) or paper_url in state.get("signals", {})
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


def collect_hacker_news(sources: dict[str, Any], state: dict[str, Any]) -> list[Signal]:
    cfg = sources.get("hacker_news", {})
    signals: list[Signal] = []
    queries = [str(q) for q in cfg.get("queries", [])]
    hits_per_query = int(cfg.get("hits_per_query", 10))
    min_points = int(cfg.get("min_points", 2))
    for query in queries:
        params = urllib.parse.urlencode({
            "query": query,
            "tags": "story",
            "hitsPerPage": hits_per_query,
        })
        url = f"https://hn.algolia.com/api/v1/search_by_date?{params}"
        data = fetch_json(url)
        hits = data.get("hits", []) if isinstance(data, dict) else []
        for hit in hits[:hits_per_query]:
            points = int(hit.get("points") or 0)
            if points < min_points:
                continue
            object_id = str(hit.get("objectID") or hit.get("id") or "").strip()
            story_url = normalize_url(hit.get("url") or (f"https://news.ycombinator.com/item?id={object_id}" if object_id else ""))
            title = clean_text(hit.get("title") or hit.get("story_title"), 500)
            if not story_url or not title:
                continue
            published = parse_datetime(hit.get("created_at"))
            seen = story_url in state.get("seen_urls", {}) or story_url in state.get("signals", {})
            comments = int(hit.get("num_comments") or 0)
            summary = f"HN query={query}; points={points}; comments={comments}"
            score, category, why, _needs = score_signal(title, summary, "hacker_news_story", 58, published, "radar", seen, ["hn", query])
            score = min(score, 74)  # HN is a community signal, never direct article authority.
            signals.append(Signal(
                title=title,
                url=story_url,
                source="Hacker News Algolia",
                source_type="hacker_news_story",
                published_at=(published or now_utc()).isoformat(),
                category="radar" if category == "veille" else category,
                score=score,
                authority=58,
                why_relevant=f"signal communautaire HN; {why}; {points} points; {comments} commentaires",
                needs_web_verification=True,
                tags=["hacker-news", "community-signal", query],
                seen_before=seen,
            ))
        time.sleep(float(cfg.get("sleep_seconds", 0.2)))
    return signals


def extract_html_title(html_text: str, fallback: str) -> str:
    og = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', html_text, flags=re.IGNORECASE)
    if og:
        return clean_text(og.group(1), 500)
    title = re.search(r"<title[^>]*>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)
    if title:
        return clean_text(title.group(1), 500)
    return fallback


def extract_html_description(html_text: str) -> str:
    meta = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', html_text, flags=re.IGNORECASE)
    if meta:
        return clean_text(meta.group(1), 600)
    return clean_text(html_text, 600)


def collect_html_watchers(sources: dict[str, Any], state: dict[str, Any]) -> list[Signal]:
    signals: list[Signal] = []
    for source in sources.get("html_watchers", []):
        url = normalize_url(source.get("url", ""))
        if not url:
            continue
        try:
            html_text = fetch_text(url, timeout=int(source.get("timeout_seconds", HTML_WATCHER_TIMEOUT_SECONDS)))
        except Exception:
            continue
        page_hash = hashlib.sha256(clean_text(html_text, 5000).encode("utf-8")).hexdigest()[:16]
        title = extract_html_title(html_text, source.get("name", "HTML watcher"))
        summary = extract_html_description(html_text)
        previous = state.get("signals", {}).get(url, {})
        seen = url in state.get("seen_urls", {}) or previous.get("page_hash") == page_hash
        authority = int(source.get("authority", 80))
        tags = list(source.get("tags", [])) + ["html-watcher", "page_hash:", f"page_hash:{page_hash}"]
        score, category, why, _needs = score_signal(title, summary, "html_watcher", authority, now_utc(), source.get("category", "veille"), seen, tags)
        score = min(score, 74)  # HTML watcher pages are change signals; require source verification.
        signals.append(Signal(
            title=title,
            url=url,
            source=source.get("name", "HTML watcher"),
            source_type="html_watcher",
            published_at=now_utc().isoformat(),
            category=category,
            score=score,
            authority=authority,
            why_relevant=f"watcher HTML; {why}; hash {page_hash}",
            needs_web_verification=True,
            tags=tags,
            seen_before=seen,
        ))
        time.sleep(float(source.get("sleep_seconds", 0.2)))
    return signals


def dedupe(signals: list[Signal]) -> list[Signal]:
    groups: list[Signal] = []
    keys_by_index: list[set[str]] = []
    for signal in signals:
        signal_keys = {f"url:{signal.url}", f"title:{normalize_title(signal.title)}"}
        matches = [idx for idx, keys in enumerate(keys_by_index) if keys & signal_keys]
        if not matches:
            groups.append(signal)
            keys_by_index.append(signal_keys)
            continue
        primary = matches[0]
        keys_by_index[primary].update(signal_keys)
        if signal.score > groups[primary].score:
            groups[primary] = signal
        for idx in reversed(matches[1:]):
            keys_by_index[primary].update(keys_by_index[idx])
            if groups[idx].score > groups[primary].score:
                groups[primary] = groups[idx]
            del groups[idx]
            del keys_by_index[idx]
    return sorted(groups, key=lambda s: (s.score, s.published_at), reverse=True)


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


def markdown_escape(value: Any) -> str:
    text = str(value or "").strip()
    text = text.replace("|", "\\|")
    return text


def recommended_action(signal: dict[str, Any]) -> str:
    decision = signal.get("editorial_decision")
    if decision == "article_candidate":
        return "verify_then_publish"
    if decision == "radar_candidate":
        return "verify_for_radar"
    return "skip"


def render_editorial_preview(payload: dict[str, Any]) -> str:
    generated_at = payload.get("generated_at", "")
    summary = payload.get("summary", {})
    policy = payload.get("policy", {})
    article_candidates = payload.get("top_article_candidates", [])
    radar_candidates = payload.get("top_radar_candidates", [])

    lines: list[str] = [
        "# Labo IA — Editorial Preview",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "## Summary",
        "",
        f"- Total signals: **{summary.get('total_signals', 0)}**",
        f"- Article candidates: **{summary.get('article_candidates', 0)}**",
        f"- Radar candidates: **{summary.get('radar_candidates', 0)}**",
        f"- Ignored: **{summary.get('ignored', 0)}**",
        f"- Errors: **{summary.get('errors', 0)}**",
        f"- X/Twitter policy: **{policy.get('x_search', 'unknown')}**",
        "",
        "## Recommended next actions",
        "",
        "1. Verify each `verify_then_publish` candidate against its source page before drafting.",
        "2. Use `verify_for_radar` items as short Radar briefs only if the source confirms a concrete recent change.",
        "3. Keep `skip` items out of the cron output; they are preserved only for auditability in JSON.",
        "",
        "## Article candidates",
        "",
    ]

    if not article_candidates:
        lines.append("No article candidate passed the current editorial bar.")
    else:
        lines.extend([
            "| Action | Score | Category | Source | Signal | Verification | URL |",
            "|---|---:|---|---|---|---|---|",
        ])
        for signal in article_candidates:
            verification = "source + freshness + non-duplicate"
            lines.append(
                "| "
                + " | ".join([
                    markdown_escape(recommended_action(signal)),
                    markdown_escape(signal.get("score")),
                    markdown_escape(signal.get("category")),
                    markdown_escape(signal.get("source")),
                    markdown_escape(signal.get("title")),
                    markdown_escape(verification),
                    markdown_escape(signal.get("url")),
                ])
                + " |"
            )

    lines.extend(["", "## Radar candidates", ""])
    if not radar_candidates:
        lines.append("No Radar candidate passed the current editorial bar.")
    else:
        lines.extend([
            "| Action | Score | Category | Source | Signal | Why not article yet | URL |",
            "|---|---:|---|---|---|---|---|",
        ])
        for signal in radar_candidates:
            lines.append(
                "| "
                + " | ".join([
                    markdown_escape(recommended_action(signal)),
                    markdown_escape(signal.get("score")),
                    markdown_escape(signal.get("category")),
                    markdown_escape(signal.get("source")),
                    markdown_escape(signal.get("title")),
                    markdown_escape(signal.get("editorial_reason")),
                    markdown_escape(signal.get("url")),
                ])
                + " |"
            )

    if payload.get("errors"):
        lines.extend(["", "## Source errors", ""])
        for error in payload["errors"]:
            lines.append(f"- **{markdown_escape(error.get('source'))}**: {markdown_escape(error.get('error'))}")

    lines.append("")
    return "\n".join(lines)


def write_editorial_preview(payload: dict[str, Any], path: Path = EDITORIAL_PREVIEW_PATH) -> Path:
    path.write_text(render_editorial_preview(payload), encoding="utf-8")
    return path


def build_debug_payload(payload: dict[str, Any]) -> dict[str, Any]:
    source_counts: dict[str, int] = {}
    decision_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    all_visible = list(payload.get("top_article_candidates", [])) + list(payload.get("top_radar_candidates", [])) + list(payload.get("signals", []))
    for signal in all_visible:
        source = str(signal.get("source", "unknown"))
        decision = str(signal.get("editorial_decision", "unknown"))
        source_type = str(signal.get("source_type", "unknown"))
        source_counts[source] = source_counts.get(source, 0) + 1
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        type_counts[source_type] = type_counts.get(source_type, 0) + 1
    return {
        "generated_at": payload.get("generated_at"),
        "summary": payload.get("summary", {}),
        "top_sources": sorted(source_counts.items(), key=lambda item: item[1], reverse=True)[:10],
        "decision_counts": decision_counts,
        "source_type_counts": type_counts,
        "article_candidates": payload.get("top_article_candidates", []),
        "radar_candidates": payload.get("top_radar_candidates", []),
        "errors": payload.get("errors", []),
    }


def render_run_report(payload: dict[str, Any]) -> str:
    debug = build_debug_payload(payload)
    summary = debug["summary"]
    lines = [
        "# Labo IA — Source Radar Run Report",
        "",
        f"Generated at: `{payload.get('generated_at')}`",
        "",
        "## Counts",
        "",
        f"- Total: **{summary.get('total_signals', 0)}**",
        f"- Article candidates: **{summary.get('article_candidates', 0)}**",
        f"- Radar candidates: **{summary.get('radar_candidates', 0)}**",
        f"- Ignored: **{summary.get('ignored', 0)}**",
        f"- Errors: **{summary.get('errors', 0)}**",
        "",
        "## Top sources",
        "",
    ]
    for source, count in debug["top_sources"]:
        lines.append(f"- {source}: {count}")
    lines.extend(["", "## Article candidates", ""])
    for signal in payload.get("top_article_candidates", []):
        lines.append(f"- **{signal.get('title')}** — {signal.get('source')} ({signal.get('score')}) — {signal.get('url')}")
    if not payload.get("top_article_candidates"):
        lines.append("- None")
    lines.extend(["", "## Radar candidates", ""])
    for signal in payload.get("top_radar_candidates", [])[:10]:
        lines.append(f"- **{signal.get('title')}** — {signal.get('source')} ({signal.get('score')}) — {signal.get('url')}")
    if payload.get("errors"):
        lines.extend(["", "## Errors", ""])
        for error in payload["errors"]:
            lines.append(f"- {error.get('source')}: {error.get('error')}")
    lines.append("")
    return "\n".join(lines)


def write_run_artifacts(payload: dict[str, Any]) -> None:
    report = render_run_report(payload)
    debug_payload = build_debug_payload(payload)
    RUN_REPORT_PATH.write_text(report, encoding="utf-8")
    DEBUG_PAYLOAD_PATH.write_text(json.dumps(debug_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    RUNS_DIR.mkdir(exist_ok=True)
    stamp = now_utc().strftime('%Y%m%dT%H%M%SZ')
    (RUNS_DIR / f"{stamp}.md").write_text(report, encoding="utf-8")
    (RUNS_DIR / f"{stamp}.debug.json").write_text(json.dumps(debug_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def status_for_signal(signal: Signal) -> str:
    if signal.editorial_decision in {"article_candidate", "radar_candidate"}:
        return "needs_review"
    return "seen"


def update_source_state(state: dict[str, Any], signals: list[Signal], *, generated_at: str) -> None:
    seen_urls = state.setdefault("seen_urls", {})
    signal_state = state.setdefault("signals", {})
    preserved_statuses = {"published", "rejected"}
    for signal in signals:
        previous = signal_state.get(signal.url, {})
        status = previous.get("status") if previous.get("status") in preserved_statuses else status_for_signal(signal)
        record = {
            "first_seen": previous.get("first_seen", generated_at),
            "last_seen": generated_at,
            "status": status,
            "source": signal.source,
            "source_type": signal.source_type,
            "title": signal.title,
            "normalized_title": normalize_title(signal.title),
            "url": signal.url,
            "score": signal.score,
            "page_hash": next((tag.split(":", 1)[1] for tag in signal.tags if tag.startswith("page_hash:") and tag != "page_hash:"), previous.get("page_hash")),
            "editorial_decision": signal.editorial_decision,
            "editorial_reason": signal.editorial_reason,
        }
        signal_state[signal.url] = record
        seen_urls[signal.url] = {
            "first_seen": record["first_seen"],
            "last_seen": generated_at,
            "status": status,
            "source": signal.source,
            "title": signal.title,
            "score": signal.score,
        }


def collect_all(*, update_state: bool, write_preview: bool = False) -> dict[str, Any]:
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

    try:
        signals.extend(collect_hacker_news(sources, state))
    except Exception as exc:
        errors.append({"source": "Hacker News Algolia", "error": f"{type(exc).__name__}: {exc}"})

    try:
        signals.extend(collect_html_watchers(sources, state))
    except Exception as exc:
        errors.append({"source": "HTML watchers", "error": f"{type(exc).__name__}: {exc}"})

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
    write_run_artifacts(payload)

    if update_state:
        update_source_state(state, reviewed, generated_at=payload["generated_at"])
        save_state(state)

    if write_preview:
        write_editorial_preview(payload)

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
    hn_query = sources.get("hacker_news", {}).get("queries", ["openai"])[0]
    checks.append((f"Hacker News Algolia {hn_query}", "https://hn.algolia.com/api/v1/search_by_date?" + urllib.parse.urlencode({
        "query": hn_query,
        "tags": "story",
        "hitsPerPage": 1,
    })))
    for source in sources.get("html_watchers", []):
        checks.append((source["name"], source["url"]))

    failed = 0
    for name, url in checks:
        try:
            text = fetch_text(url, timeout=12)
            print(f"OK   {name}: {len(text)} bytes")
        except Exception as exc:
            failed += 1
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect AI source signals for Labo IA")
    parser.add_argument("--check-sources", action="store_true", help="Fetch each configured source once and print OK/FAIL")
    parser.add_argument("--dry-run-editorial", action="store_true", help="Generate automation/editorial_preview.md for human review")
    parser.add_argument("--update-state", action="store_true", help="Mark current URLs as seen after collection")
    args = parser.parse_args()

    if args.check_sources:
        return check_sources()

    payload = collect_all(update_state=args.update_state, write_preview=args.dry_run_editorial)
    print(json.dumps(payload["summary"], indent=2, ensure_ascii=False))
    if args.dry_run_editorial:
        print(f"Editorial preview: {EDITORIAL_PREVIEW_PATH}")
    if payload.get("errors"):
        print("Errors:", json.dumps(payload["errors"], indent=2, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
