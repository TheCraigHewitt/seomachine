import importlib.util
import sys
import types
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "research_quick_wins.py"


def load_research_quick_wins_module():
    fake_dotenv = types.ModuleType("dotenv")
    fake_dotenv.load_dotenv = lambda *args, **kwargs: None

    modules_pkg = types.ModuleType("modules")

    google_search_console = types.ModuleType("modules.google_search_console")
    google_search_console.GoogleSearchConsole = object
    dataforseo = types.ModuleType("modules.dataforseo")
    dataforseo.DataForSEO = object
    google_analytics = types.ModuleType("modules.google_analytics")
    google_analytics.GoogleAnalytics = object
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
        "modules.google_analytics": google_analytics,
        "modules.opportunity_scorer": opportunity_scorer,
        "modules.search_intent_analyzer": search_intent,
    }
    previous = {name: sys.modules.get(name) for name in injected}
    sys.modules.update(injected)
    try:
        spec = importlib.util.spec_from_file_location(
            "research_quick_wins_under_test", MODULE_PATH
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


class QuickWinsHelperTests(unittest.TestCase):
    def test_get_first_ranking_returns_first_dict_only(self):
        module = load_research_quick_wins_module()

        self.assertEqual(module.get_first_ranking([{"position": 11}]), {"position": 11})
        self.assertIsNone(module.get_first_ranking([]))
        self.assertIsNone(module.get_first_ranking([None]))

    def test_get_serp_features_returns_empty_list_on_provider_error(self):
        module = load_research_quick_wins_module()

        class FakeDFS:
            def get_serp_data(self, keyword, limit=10):
                raise RuntimeError("api down")

        self.assertEqual(
            module.get_serp_features(FakeDFS(), "podcast monetization"), []
        )

    def test_get_serp_features_extracts_feature_list(self):
        module = load_research_quick_wins_module()

        class FakeDFS:
            def get_serp_data(self, keyword, limit=10):
                return {"features": ["people_also_ask", "featured_snippet"]}

        self.assertEqual(
            module.get_serp_features(FakeDFS(), "podcast monetization"),
            ["people_also_ask", "featured_snippet"],
        )


if __name__ == "__main__":
    unittest.main()
