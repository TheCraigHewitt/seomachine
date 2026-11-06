"""Synthetic MCP responses exercise the real RPC parser and module CLI."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock

import requests

from data_sources.modules.parallel_search import ParallelSearch, ParallelSearchError


PASSAGE = "Before\u0085next\u2028line\u2029after"
RESULT = {"structuredContent": {"results": [
    {"title": "Synthetic guide", "url": "https://example.org/guide", "excerpts": [PASSAGE]}
]}}


def response_for(message, newline="\n", multiline=False, sse=True):
    response = requests.Response()
    response.status_code = 200
    serialized = json.dumps(message, ensure_ascii=False, indent=2 if multiline else None)
    if sse:
        # Split only the pretty printer's LF, retaining literal Unicode separators.
        lines = [": synthetic heartbeat", "", "event: message"]
        lines.extend("data: " + line for line in serialized.split("\n"))
        response._content = (newline.join(lines) + newline * 2).encode("utf-8")
        response.headers["Content-Type"] = "text/event-stream"
    else:
        response._content = serialized.encode("utf-8")
        response.headers["Content-Type"] = "application/json; charset=utf-8"
    response._content_consumed = True
    return response


# A subprocess startup hook supplies synthetic HTTP responses only. The CLI,
# requests preparation, RPC parser, and result formatting remain production code.
CLI_TRANSPORT = '''
import json
import os
import requests.adapters
from test_parallel_search_sse import response_for, RESULT

def synthetic_send(adapter, request, **kwargs):
    payload = json.loads(request.body) if request.body else {}
    method = payload.get("method")
    if method == "initialize":
        result = {"protocolVersion": "2025-03-26"}
    elif method == "tools/list":
        result = {"tools": [{"name": "web_search"}]}
    else:
        result = RESULT
    response = response_for({"id": payload.get("id"), "result": result},
                            newline=os.environ["SYNTHETIC_SSE_NEWLINE"], multiline=True)
    response.request = request
    response.headers["Mcp-Session-Id"] = "synthetic-session"
    return response
requests.adapters.HTTPAdapter.send = synthetic_send
'''


class ParallelSearchSSETests(unittest.TestCase):
    def rpc(self, message, **kwargs):
        session = Mock()
        session.headers = {}
        response = response_for(message, **kwargs)
        session.post.return_value.__enter__ = Mock(return_value=response)
        session.post.return_value.__exit__ = Mock(return_value=False)
        return ParallelSearch()._rpc(session, "tools/call", 3, {})

    def test_rpc_preserves_literal_unicode_separators_with_sse_line_endings(self):
        for newline in ["\n", "\r\n", "\r"]:
            for multiline in [False, True]:
                with self.subTest(newline=repr(newline), multiline=multiline):
                    result = self.rpc({"id": 3, "result": RESULT}, newline=newline,
                                      multiline=multiline)
                    self.assertEqual(result, RESULT)
                    self.assertEqual(ParallelSearch._process_results(result, 1)["results"][0]["content"],
                                     PASSAGE)

    def test_rpc_json_preserves_literal_unicode_separators(self):
        self.assertEqual(self.rpc({"id": 3, "result": RESULT}, sse=False), RESULT)

    def test_rpc_errors_keep_working_with_all_sse_line_endings(self):
        for newline in ["\n", "\r\n", "\r"]:
            with self.subTest(newline=repr(newline)):
                with self.assertRaisesRegex(ParallelSearchError, "RPC error"):
                    self.rpc({"id": 3, "error": {"message": PASSAGE}}, newline=newline,
                             multiline=True)
                with self.assertRaisesRegex(ParallelSearchError, "Missing"):
                    self.rpc({"id": 999, "result": RESULT}, newline=newline)

    def test_rpc_malformed_sse_json_is_still_an_error(self):
        response = response_for({"id": 3, "result": RESULT})
        response._content = b'data: {invalid}\r\r'
        session = Mock()
        session.headers = {}
        session.post.return_value.__enter__ = Mock(return_value=response)
        session.post.return_value.__exit__ = Mock(return_value=False)
        with self.assertRaisesRegex(ParallelSearchError, "Malformed"):
            ParallelSearch()._rpc(session, "tools/call", 3, {})

    def test_native_module_cli_preserves_unicode_from_multiline_sse(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, "sitecustomize.py").write_text(CLI_TRANSPORT)
            # Preserve the sandbox proxy and other network environment settings.
            env = os.environ.copy()
            for name in ["PARALLEL_API_KEY", "EXA_API_KEY", "PARALLEL_SEARCH_ENABLED"]:
                env.pop(name, None)
            env["PYTHONPATH"] = os.pathsep.join([temp, str(repo / "tests"), str(repo)])
            for newline in ["\n", "\r\n", "\r"]:
                with self.subTest(newline=repr(newline)):
                    env["SYNTHETIC_SSE_NEWLINE"] = newline
                    completed = subprocess.run(
                        [sys.executable, "-m", "data_sources.modules.parallel_search",
                         "best podcast hosting platforms for beginners", "--num-results", "3"],
                        cwd=repo, env=env, capture_output=True, encoding="utf-8", timeout=15)
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    self.assertEqual(json.loads(completed.stdout), {"results": [{
                        "title": "Synthetic guide", "url": "https://example.org/guide",
                        "content": PASSAGE}], "total_results": 1})


if __name__ == "__main__":
    unittest.main()
