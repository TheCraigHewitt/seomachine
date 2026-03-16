import importlib.util
import sys
import types
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data_sources"
    / "modules"
    / "google_analytics.py"
)


def load_google_analytics_module():
    fake_google_analytics = types.ModuleType("google.analytics")
    fake_google_analytics_v1beta = types.ModuleType("google.analytics.data_v1beta")
    fake_google_analytics_types = types.ModuleType("google.analytics.data_v1beta.types")
    fake_google_oauth2 = types.ModuleType("google.oauth2")
    fake_service_account = types.SimpleNamespace(
        Credentials=types.SimpleNamespace(
            from_service_account_file=lambda *args, **kwargs: None
        )
    )

    fake_google_analytics_v1beta.BetaAnalyticsDataClient = object
    for name in [
        "DateRange",
        "Dimension",
        "Metric",
        "RunReportRequest",
        "FilterExpression",
        "Filter",
    ]:
        setattr(fake_google_analytics_types, name, object)
    fake_google_oauth2.service_account = fake_service_account

    modules = {
        "google.analytics": fake_google_analytics,
        "google.analytics.data_v1beta": fake_google_analytics_v1beta,
        "google.analytics.data_v1beta.types": fake_google_analytics_types,
        "google.oauth2": fake_google_oauth2,
    }

    previous = {name: sys.modules.get(name) for name in modules}
    sys.modules.update(modules)
    try:
        spec = importlib.util.spec_from_file_location(
            "google_analytics_under_test", MODULE_PATH
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


class GoogleAnalyticsCompatTests(unittest.TestCase):
    def test_get_page_performance_returns_exact_match_and_aliases_engagement(self):
        module = load_google_analytics_module()
        ga = object.__new__(module.GoogleAnalytics)

        ga.get_top_pages = lambda days=30, limit=20, path_filter="/blog/": [
            {
                "path": "/blog/post-a",
                "pageviews": 100,
                "avg_session_duration": 12.0,
                "avg_engagement_time": 12.0,
                "bounce_rate": 0.25,
            },
            {
                "path": "/blog/post-b",
                "pageviews": 50,
                "avg_session_duration": 6.0,
                "avg_engagement_time": 6.0,
                "bounce_rate": 0.10,
            },
        ]

        page = ga.get_page_performance("/blog/post-b", days=45)

        self.assertEqual(page["path"], "/blog/post-b")
        self.assertEqual(page["pageviews"], 50)
        self.assertEqual(page["avg_engagement_time"], 6.0)

    def test_get_page_performance_returns_empty_dict_when_no_pages_match(self):
        module = load_google_analytics_module()
        ga = object.__new__(module.GoogleAnalytics)
        ga.get_top_pages = lambda **kwargs: []

        self.assertEqual(ga.get_page_performance("/blog/missing"), {})


if __name__ == "__main__":
    unittest.main()
