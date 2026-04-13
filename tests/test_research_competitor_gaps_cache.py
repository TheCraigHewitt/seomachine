import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch


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


class RelevantKeywordCacheTests(unittest.TestCase):
    def test_relevant_terms_config_is_loaded_once_for_multiple_keywords(self):
        module = load_research_competitor_gaps_module()
        module._RELEVANT_TERMS_CACHE = None

        file_data = '{"relevant_terms": ["seo", "content"]}'
        with patch.object(module.os.path, "exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=file_data)
        ) as mocked_open:
            self.assertTrue(module.is_relevant_keyword("best seo tools"))
            self.assertTrue(module.is_relevant_keyword("content strategy guide"))
            self.assertFalse(module.is_relevant_keyword("gardening checklist"))

        self.assertEqual(mocked_open.call_count, 1)

    def test_empty_relevant_terms_means_no_filter(self):
        module = load_research_competitor_gaps_module()
        module._RELEVANT_TERMS_CACHE = None

        with patch.object(module.os.path, "exists", return_value=True), patch(
            "builtins.open", mock_open(read_data='{"relevant_terms": []}')
        ) as mocked_open:
            self.assertTrue(module.is_relevant_keyword("any broad keyword"))
            self.assertTrue(module.is_relevant_keyword("another long keyword"))

        self.assertEqual(mocked_open.call_count, 1)


if __name__ == "__main__":
    unittest.main()
