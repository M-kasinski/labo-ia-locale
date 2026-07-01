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


if __name__ == "__main__":
    unittest.main()
