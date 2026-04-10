import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "data_sources" / "modules" / "dataforseo.py"
)


def load_dataforseo_module():
    spec = importlib.util.spec_from_file_location("dataforseo_under_test", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DataForSEOResilienceTests(unittest.TestCase):
    def setUp(self) -> None:
        module = load_dataforseo_module()
        self.client = object.__new__(module.DataForSEO)

    def test_get_serp_data_returns_task_error_when_result_is_missing(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [{"status_code": 20000, "result": []}],
        }

        result = self.client.get_serp_data("test keyword")

        self.assertEqual(result, {"error": "Task returned no results"})

    def test_get_keyword_ideas_returns_empty_list_when_result_is_missing(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [{"status_code": 20000, "result": []}],
        }

        result = self.client.get_keyword_ideas("seed keyword")

        self.assertEqual(result, [])

    def test_analyze_competitor_handles_missing_result_without_crashing(self):
        self.client._post = lambda endpoint, data: {
            "status_code": 20000,
            "tasks": [
                {
                    "status_code": 20000,
                    "data": {"keyword": "keyword one"},
                    "result": [],
                }
            ],
        }

        result = self.client.analyze_competitor(
            "competitor.com", ["keyword one"], your_domain="example.com"
        )

        self.assertEqual(result["comparison"], [])


if __name__ == "__main__":
    unittest.main()
