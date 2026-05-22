import importlib.util
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "research_competitor_gaps.py"


def load_research_competitor_gaps_module():
    fake_dotenv = types.ModuleType("dotenv")
    fake_dotenv.load_dotenv = lambda *args, **kwargs: None

    modules_pkg = types.ModuleType("modules")
    google_search_console = types.ModuleType("modules.google_search_console")
    google_search_console.GoogleSearchConsole = object
    dataforseo = types.ModuleType("modules.dataforseo")
    dataforseo.DataForSEO = object
    opportunity_scorer = types.ModuleType("modules.opportunity_scorer")
    opportunity_scorer.OpportunityScorer = object
    opportunity_scorer.OpportunityType = object
    search_intent = types.ModuleType("modules.search_intent_analyzer")
    search_intent.SearchIntentAnalyzer = object

    injected = {
        "dotenv": fake_dotenv,
        "modules": modules_pkg,
        "modules.google_search_console": google_search_console,
        "modules.dataforseo": dataforseo,
        "modules.opportunity_scorer": opportunity_scorer,
        "modules.search_intent_analyzer": search_intent,
    }
    previous = {name: sys.modules.get(name) for name in injected}
    sys.modules.update(injected)
    try:
        spec = importlib.util.spec_from_file_location(
            "research_competitor_gaps_under_test", MODULE_PATH
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load {MODULE_PATH}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, value in previous.items():
            if value is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = value


class CompetitorGapsReportTests(unittest.TestCase):
    def test_write_markdown_report_handles_missing_difficulty_values(self):
        module = load_research_competitor_gaps_module()
        gaps = [
            {
                "keyword": "podcast analytics",
                "priority": "HIGH",
                "opportunity_score": 88.0,
                "competitor": "example.com",
                "competitor_type": "Content",
                "competitor_position": 4,
                "search_volume": 1200,
                "your_position": None,
                "search_intent": "informational",
                "content_type": "Guide/Article",
                "score_breakdown": {
                    "volume_score": 90,
                    "competition_score": 75,
                    "intent_score": 80,
                },
            },
            {
                "keyword": "podcast monetization",
                "priority": "MEDIUM",
                "opportunity_score": 65.0,
                "competitor": "competitor.com",
                "competitor_type": "Direct",
                "competitor_position": 8,
                "search_volume": 300,
                "difficulty": None,
                "your_position": None,
                "search_intent": "commercial",
                "content_type": "How-To Guide",
            },
        ]

        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                Path("research").mkdir()

                module.write_markdown_report(gaps, total_found=2)

                [report] = Path("research").glob("competitor-gaps-*.md")
                content = report.read_text()
                self.assertIn("- **Average SEO Difficulty:** N/A", content)
                self.assertIn("- **Total Potential Search Volume:** 1,500/month", content)
            finally:
                os.chdir(old_cwd)

    def test_write_markdown_report_averages_zero_difficulty_values(self):
        module = load_research_competitor_gaps_module()
        gaps = [
            {
                "keyword": "easy podcast seo",
                "priority": "CRITICAL",
                "opportunity_score": 91.0,
                "competitor": "example.com",
                "competitor_type": "Content",
                "competitor_position": 2,
                "search_volume": 100,
                "difficulty": 0,
                "your_position": None,
                "search_intent": "informational",
                "content_type": "Guide/Article",
            },
            {
                "keyword": "hard podcast seo",
                "priority": "HIGH",
                "opportunity_score": 82.0,
                "competitor": "example.org",
                "competitor_type": "Content",
                "competitor_position": 5,
                "search_volume": 100,
                "difficulty": 50,
                "your_position": None,
                "search_intent": "informational",
                "content_type": "Guide/Article",
            },
        ]

        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                Path("research").mkdir()

                module.write_markdown_report(gaps, total_found=2)

                [report] = Path("research").glob("competitor-gaps-*.md")
                self.assertIn(
                    "- **Average SEO Difficulty:** 25.0/100", report.read_text()
                )
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
