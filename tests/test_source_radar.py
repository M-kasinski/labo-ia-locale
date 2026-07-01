from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "automation" / "collect_ai_sources.py"
spec = importlib.util.spec_from_file_location("collect_ai_sources", MODULE_PATH)
assert spec is not None
collector = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = collector
spec.loader.exec_module(collector)


def make_signal(**overrides):
    base = dict(
        title="llama.cpp b9856",
        url="https://github.com/ggml-org/llama.cpp/releases/tag/b9856",
        source="llama.cpp",
        source_type="github_release",
        published_at=datetime.now(timezone.utc).isoformat(),
        category="local",
        score=107,
        authority=95,
        why_relevant="source primaire structurée",
        needs_web_verification=False,
        tags=["local-inference", "gguf", "runtime"],
        seen_before=False,
    )
    base.update(overrides)
    return collector.Signal(**base)


class SourceRadarEditorialReviewTests(unittest.TestCase):
    def test_editorial_decision_ignores_bare_version_release_without_substance(self):
        signal = make_signal(title="b9856", score=107)

        reviewed = collector.apply_editorial_review([signal], existing_topics=set())[0]

        self.assertEqual(reviewed.editorial_decision, "ignore")
        self.assertEqual(reviewed.editorial_reason, "version-only release without substantive signal")
        self.assertLess(reviewed.score, 75)

    def test_editorial_decision_keeps_substantive_runtime_release_as_article_candidate(self):
        signal = make_signal(
            title="llama.cpp b9856: CUDA graph capture improves batched inference",
            score=107,
            why_relevant="release GitHub officielle; performance; CUDA; inference",
        )

        reviewed = collector.apply_editorial_review([signal], existing_topics=set())[0]

        self.assertEqual(reviewed.editorial_decision, "article_candidate")
        self.assertGreaterEqual(reviewed.score, 75)

    def test_editorial_decision_marks_existing_topic_as_duplicate_ignore(self):
        signal = make_signal(
            title="Ollama v0.31.1 launch agents llama.cpp",
            url="https://github.com/ollama/ollama/releases/tag/v0.31.1",
            source="Ollama",
            score=115,
        )

        reviewed = collector.apply_editorial_review([signal], existing_topics={"ollama", "llama", "cpp"})[0]

        self.assertEqual(reviewed.editorial_decision, "ignore")
        self.assertEqual(reviewed.editorial_reason, "likely duplicate of existing article topic")

    def test_build_shortlists_limits_and_separates_article_and_radar_candidates(self):
        article_signals = [
            make_signal(title=f"MLX release improves Apple Silicon inference {i}", score=90 - i)
            for i in range(8)
        ]
        radar_signals = [
            make_signal(
                title=f"arXiv paper on agent memory {i}",
                source_type="arxiv_paper",
                source="arXiv cs.CL",
                category="radar",
                score=65 - i,
                needs_web_verification=True,
            )
            for i in range(12)
        ]
        reviewed = collector.apply_editorial_review(article_signals + radar_signals, existing_topics=set())

        shortlists = collector.build_shortlists(reviewed, max_articles=5, max_radar=10)

        self.assertEqual(len(shortlists["top_article_candidates"]), 5)
        self.assertEqual(len(shortlists["top_radar_candidates"]), 10)
        self.assertTrue(all(item["editorial_decision"] == "article_candidate" for item in shortlists["top_article_candidates"]))
        self.assertTrue(all(item["editorial_decision"] == "radar_candidate" for item in shortlists["top_radar_candidates"]))

    def test_render_editorial_preview_contains_actions_and_source_links(self):
        signal = make_signal(
            title="MLX release improves Apple Silicon inference",
            url="https://github.com/ml-explore/mlx/releases/tag/v1.2.3",
            source="MLX",
            score=90,
        )
        reviewed = collector.apply_editorial_review([signal], existing_topics=set())
        shortlists = collector.build_shortlists(reviewed, max_articles=5, max_radar=10)
        payload = {
            "generated_at": "2026-07-01T12:00:00+00:00",
            "summary": {"total_signals": 1, "article_candidates": 1, "radar_candidates": 0, "ignored": 0, "errors": 0},
            "policy": {"x_search": "disabled / not used"},
            **shortlists,
            "errors": [],
        }

        markdown = collector.render_editorial_preview(payload)

        self.assertIn("# Labo IA — Editorial Preview", markdown)
        self.assertIn("verify_then_publish", markdown)
        self.assertIn("MLX release improves Apple Silicon inference", markdown)
        self.assertIn("https://github.com/ml-explore/mlx/releases/tag/v1.2.3", markdown)
        self.assertIn("X/Twitter policy: **disabled / not used**", markdown)

    def test_collect_hn_algolia_turns_recent_story_into_low_confidence_radar_signal(self):
        sources = {"hacker_news": {"queries": ["openai"], "hits_per_query": 5, "min_points": 2}}
        state = {"signals": {}, "seen_urls": {}}
        def fake_json(url):
            self.assertIn("hn.algolia.com/api/v1/search_by_date", url)
            return {"hits": [{
                "title": "OpenAI Codex CLI adds agent workflow",
                "url": "https://news.ycombinator.com/item?id=123",
                "objectID": "123",
                "created_at": "2026-07-01T11:00:00Z",
                "points": 42,
                "num_comments": 9,
            }]}

        original_fetch_json = collector.fetch_json
        try:
            collector.fetch_json = fake_json
            signals = collector.collect_hacker_news(sources, state)
        finally:
            collector.fetch_json = original_fetch_json

        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].source, "Hacker News Algolia")
        self.assertEqual(signals[0].category, "radar")
        self.assertTrue(signals[0].needs_web_verification)
        self.assertLess(signals[0].score, 75)

    def test_update_source_state_tracks_needs_review_seen_and_preserves_published(self):
        candidate = make_signal(title="OpenAI Codex agent workflow", url="https://example.com/codex", score=90)
        ignored = make_signal(title="b9856", url="https://example.com/b9856", score=49, editorial_decision="ignore")
        reviewed = collector.apply_editorial_review([candidate, ignored], existing_topics=set())
        state = {"signals": {"https://example.com/codex": {"status": "published", "title": "old"}}, "seen_urls": {}}

        collector.update_source_state(state, reviewed, generated_at="2026-07-01T12:00:00+00:00")

        self.assertEqual(state["signals"]["https://example.com/codex"]["status"], "published")
        self.assertEqual(state["signals"]["https://example.com/b9856"]["status"], "seen")
        self.assertIn("https://example.com/codex", state["seen_urls"])

    def test_dedupe_prefers_best_signal_by_url_and_normalized_title(self):
        first = make_signal(title="OpenAI Codex agent workflow", url="https://example.com/a", score=50)
        duplicate_title = make_signal(title="OpenAI: Codex agent workflow!", url="https://example.com/b", score=80)
        duplicate_url = make_signal(title="Different title", url="https://example.com/a", score=90)

        deduped = collector.dedupe([first, duplicate_title, duplicate_url])

        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0].score, 90)

    def test_collect_html_watchers_extracts_title_and_hashes_page(self):
        sources = {"html_watchers": [{
            "name": "Anthropic News",
            "url": "https://www.anthropic.com/news",
            "category": "veille",
            "authority": 88,
            "tags": ["anthropic", "claude"],
        }]}
        state = {"signals": {}, "seen_urls": {}}
        html = """<html><head><title>Claude Code gets better hooks</title><meta name='description' content='Anthropic updates Claude Code for agents'></head><body>Claude Code agent update</body></html>"""
        original_fetch_text = collector.fetch_text
        try:
            collector.fetch_text = lambda url, timeout=20: html
            signals = collector.collect_html_watchers(sources, state)
        finally:
            collector.fetch_text = original_fetch_text

        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].source_type, "html_watcher")
        self.assertEqual(signals[0].source, "Anthropic News")
        self.assertIn("page_hash:", signals[0].tags)
        self.assertTrue(signals[0].needs_web_verification)

    def test_render_run_report_and_debug_payload_include_sources_and_counts(self):
        payload = {
            "generated_at": "2026-07-01T12:00:00+00:00",
            "summary": {"total_signals": 2, "article_candidates": 1, "radar_candidates": 1, "ignored": 0, "errors": 0},
            "top_article_candidates": [{"title": "Article", "source": "OpenAI News", "score": 90, "url": "https://example.com/a"}],
            "top_radar_candidates": [{"title": "Radar", "source": "Hacker News Algolia", "score": 60, "url": "https://example.com/r"}],
            "signals": [],
            "errors": [],
        }

        report = collector.render_run_report(payload)
        debug_payload = collector.build_debug_payload(payload)

        self.assertIn("# Labo IA — Source Radar Run Report", report)
        self.assertIn("OpenAI News", report)
        self.assertEqual(debug_payload["summary"]["total_signals"], 2)
        self.assertEqual(debug_payload["top_sources"][0][0], "OpenAI News")


if __name__ == "__main__":
    unittest.main()
