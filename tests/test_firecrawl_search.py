import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data_sources"
    / "modules"
    / "firecrawl_search.py"
)


def load_firecrawl_search_module():
    spec = importlib.util.spec_from_file_location(
        "firecrawl_search_under_test", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeFirecrawlClient:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def search(self, query, **kwargs):
        self.calls.append((query, kwargs))
        return self.response


class FirecrawlSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        module = load_firecrawl_search_module()
        self.client = object.__new__(module.FirecrawlSearch)

    def use_response(self, web=None, news=None):
        fake = FakeFirecrawlClient(SimpleNamespace(web=web, news=news))
        self.client.client = fake
        return fake

    def test_search_sends_integration_tag(self):
        fake = self.use_response(web=[])

        self.client.search("podcast hosting", num_results=5)

        query, kwargs = fake.calls[0]
        self.assertEqual(query, "podcast hosting")
        self.assertEqual(kwargs["integration"], "_seomachine")
        self.assertEqual(kwargs["limit"], 5)
        self.assertNotIn("scrape_options", kwargs)

    def test_helpers_send_integration_tag(self):
        fake = self.use_response(web=[])

        self.client.find_competitor_content("podcast", ["competitor.com"])
        self.client.discover_content_ideas("podcast", days_back=30)

        for _, kwargs in fake.calls:
            self.assertEqual(kwargs["integration"], "_seomachine")
        self.assertEqual(fake.calls[0][1]["include_domains"], ["competitor.com"])
        self.assertTrue(fake.calls[1][1]["tbs"].startswith("cdr:1,cd_min:"))

    def test_search_maps_web_and_news_results(self):
        self.use_response(
            web=[
                SimpleNamespace(
                    url="https://www.example.com/a",
                    title="A",
                    description="Snippet A",
                )
            ],
            news=[
                SimpleNamespace(
                    url="https://news.example.com/b",
                    title="B",
                    snippet="Snippet B",
                    date="2 days ago",
                )
            ],
        )

        result = self.client.search("podcast", include_news=True)

        self.assertEqual(result["total_results"], 2)
        self.assertEqual(result["results"][0]["content"], "Snippet A")
        self.assertEqual(result["results"][1]["content"], "Snippet B")
        self.assertEqual(result["results"][1]["published_date"], "2 days ago")

    def test_markdown_mode_reads_document_metadata(self):
        fake = self.use_response(
            web=[
                SimpleNamespace(
                    markdown="# Page",
                    metadata=SimpleNamespace(
                        url=None,
                        source_url="https://example.com/page",
                        title="Page",
                        published_time=None,
                    ),
                ),
                SimpleNamespace(markdown="# No URL", metadata=None),
            ]
        )

        result = self.client.search("podcast", content_mode="markdown")

        self.assertEqual(
            fake.calls[0][1]["scrape_options"]["formats"], ["markdown"]
        )
        self.assertEqual(
            result["results"],
            [
                {
                    "title": "Page",
                    "url": "https://example.com/page",
                    "content": "# Page",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
