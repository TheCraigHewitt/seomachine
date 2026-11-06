import json
import os
import unittest
from unittest.mock import patch

import requests

from data_sources.modules.parallel_search import ParallelSearch, ParallelSearchError
from data_sources.modules.exa_search import ExaSearch


RESULTS = {"results": [
    {"url": "https://example.org/guide", "title": "Guide", "excerpts": ["First passage", "Café"],
     "publish_date": "2026-01-01"},
    {"url": "https://example.org/other", "title": None, "excerpts": []},
]}


class ParallelSearchTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.sent = []
        self.call_result = {"structuredContent": RESULTS}
        self.fail_method = None
        self.status = 200
        self.sse = True
        self.rpc_error = False
        self.redirect_flags = []
        self.real_send = requests.Session.send

        def session_send(session, request, **kwargs):
            self.redirect_flags.append(kwargs.get("allow_redirects"))
            return self.real_send(session, request, **kwargs)

        self.send_patch = patch.object(requests.Session, "send", session_send)
        self.send_patch.start()
        self.addCleanup(self.send_patch.stop)
        self.adapter = patch.object(requests.adapters.HTTPAdapter, "send", self.respond)
        self.adapter.start()
        self.addCleanup(self.adapter.stop)

    def respond(self, request, **kwargs):
        self.sent.append(request)
        payload = json.loads(request.body) if request.body else {}
        method = payload.get("method")
        response = requests.Response()
        response.request = request
        response.status_code = self.status if method == self.fail_method else 200
        response.headers["Mcp-Session-Id"] = "test-session"
        if method == "initialize":
            result = {"protocolVersion": ParallelSearch.PROTOCOL_VERSION}
        elif method == "tools/list":
            result = {"tools": [{"name": "web_search"}]}
        else:
            result = self.call_result
        message = {"jsonrpc": "2.0", "id": payload.get("id"), "result": result}
        if self.rpc_error and method == "tools/call":
            message = {"id": payload["id"], "error": {"code": -1}}
        if self.sse:
            response.headers["Content-Type"] = "text/event-stream"
            response._content = (": heartbeat\r\n\r\nevent: message\r\ndata: " +
                                 json.dumps(message, ensure_ascii=False) + "\r\n\r\n").encode()
        else:
            response.headers["Content-Type"] = "application/json"
            response._content = json.dumps(message).encode()
        return response

    def test_search_shape_limit_utf8_and_all_prepared_headers(self):
        result = ParallelSearch().search("podcast hosting beginners", num_results=1)
        self.assertEqual(result, {"results": [{"title": "Guide", "url": "https://example.org/guide",
                          "content": "First passage\nCafé", "published_date": "2026-01-01"}],
                          "total_results": 1})
        self.assertEqual([r.method for r in self.sent], ["POST"] * 4 + ["DELETE"])
        self.assertEqual([json.loads(r.body)["method"] for r in self.sent[:-1]],
                         ["initialize", "notifications/initialized", "tools/list", "tools/call"])
        for request in self.sent:
            self.assertEqual(request.headers["User-Agent"], ParallelSearch.USER_AGENT)
            self.assertNotIn("Authorization", request.headers)
        self.assertTrue(all(flag is False for flag in self.redirect_flags))
        self.assertEqual(self.sent[-1].headers["Mcp-Session-Id"], "test-session")
        self.assertEqual(json.loads(self.sent[3].body)["params"]["arguments"],
                         {"objective": "podcast hosting beginners", "search_queries": ["podcast hosting beginners"]})

    def test_json_and_text_content_fallback(self):
        self.sse = False
        self.call_result = {"content": [{"type": "text", "text": json.dumps(RESULTS)}]}
        result = ParallelSearch().search("podcast hosting")
        self.assertEqual(result["total_results"], 2)
        self.assertEqual(result["results"][1]["title"], "No Title")

    def test_explicit_key_wins_and_applies_to_teardown(self):
        os.environ["PARALLEL_API_KEY"] = "environment-test-value"
        ParallelSearch(api_key="explicit-test-value").search("podcast hosting")
        for request in self.sent:
            self.assertEqual(request.headers["Authorization"], "Bearer explicit-test-value")

    def test_environment_key_and_explicit_empty_key(self):
        os.environ["PARALLEL_API_KEY"] = "environment-test-value"
        self.assertEqual(ParallelSearch().api_key, "environment-test-value")
        with self.assertRaises(ValueError):
            ParallelSearch(api_key="")
        os.environ["PARALLEL_API_KEY"] = " "
        with self.assertRaises(ValueError):
            ParallelSearch()
        self.assertEqual(self.sent, [])

    def test_disabled_offline_and_environment_optout_do_not_send(self):
        for client in [ParallelSearch(enabled=False), ParallelSearch(offline=True)]:
            with self.assertRaises(ParallelSearchError):
                client.search("podcast hosting")
        os.environ["PARALLEL_SEARCH_ENABLED"] = "false"
        with self.assertRaises(ParallelSearchError):
            ParallelSearch().search("podcast hosting")
        self.assertEqual(self.sent, [])

    def test_invalid_queries_limits_and_timeout_do_not_send(self):
        for query, limit in [("", 1), (None, 1), ("podcast", 0), ("podcast", 11), ("podcast", True)]:
            with self.assertRaises(ValueError):
                ParallelSearch().search(query, limit)
        with self.assertRaises(ValueError):
            ParallelSearch(timeout=0)
        self.assertEqual(self.sent, [])

    def test_http_failures_are_not_retried_or_downgraded_to_anonymous(self):
        for status in [401, 403, 429, 500]:
            self.sent.clear()
            self.fail_method, self.status = "tools/call", status
            with self.assertRaises(requests.HTTPError):
                ParallelSearch(api_key="invalid-test-value").search("podcast hosting")
            self.assertEqual(len(self.sent), 5)
            self.assertEqual(self.sent[-1].method, "DELETE")
            self.assertTrue(all(r.headers["Authorization"] == "Bearer invalid-test-value" for r in self.sent))

    def test_redirect_is_rejected(self):
        self.fail_method, self.status = "initialize", 307
        with self.assertRaisesRegex(ParallelSearchError, "redirect"):
            ParallelSearch().search("podcast hosting")
        self.assertEqual(len(self.sent), 1)

    def test_rpc_and_tool_errors_are_not_empty_success(self):
        self.rpc_error = True
        with self.assertRaisesRegex(ParallelSearchError, "RPC"):
            ParallelSearch().search("podcast hosting")
        self.rpc_error = False
        self.call_result = {"isError": True, "content": [{"type": "text", "text": "Failure"}]}
        with self.assertRaisesRegex(ParallelSearchError, "failed"):
            ParallelSearch().search("podcast hosting")

    def test_empty_results_and_malformed_data(self):
        self.assertEqual(ParallelSearch._process_results({"structuredContent": {"results": []}}, 1),
                         {"results": [], "total_results": 0})
        for data in [{}, {"results": None}, {"results": [{"url": "https://example.org", "excerpts": "bad"}]}]:
            with self.assertRaises(ParallelSearchError):
                ParallelSearch._process_results({"structuredContent": data}, 1)
        with self.assertRaises(ParallelSearchError):
            ParallelSearch._process_results({"content": [{"type": "text", "text": "not JSON"}]}, 1)

    def test_timeout_propagates_and_closes_session(self):
        original_respond = self.respond

        def timeout_on_search(adapter, request, **kwargs):
            if request.body and json.loads(request.body).get("method") == "tools/call":
                raise requests.Timeout("recorded timeout")
            return original_respond(request, **kwargs)

        with patch.object(requests.adapters.HTTPAdapter, "send", timeout_on_search):
            with self.assertRaises(requests.Timeout):
                ParallelSearch().search("podcast hosting")
        self.assertEqual(self.sent[-1].method, "DELETE")

    def test_existing_exa_still_requires_its_own_key(self):
        with self.assertRaisesRegex(ValueError, "EXA_API_KEY must be set"):
            ExaSearch()
        self.assertEqual(self.sent, [])


if __name__ == "__main__":
    unittest.main()
