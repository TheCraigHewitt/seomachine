"""Real local HTTP fixtures with synthetic MCP payloads and bounded open streams."""

from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from threading import Event, Thread
import unittest

import requests

from data_sources.modules.parallel_search import ParallelSearch, ParallelSearchError


PASSAGE = "Before\u0085next\u2028line\u2029after"
RESULT = {"structuredContent": {"results": [
    {"title": "Synthetic guide", "url": "https://example.org/guide", "excerpts": [PASSAGE]}
]}}


@contextmanager
def http_fixture(body, media_type, *, hold_open=True, content_length=False):
    flushed, release = Event(), Event()

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", "0")))
            self.send_response(200)
            self.send_header("Content-Type", media_type)
            self.send_header("Connection", "close")
            if content_length:
                self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            self.wfile.flush()
            flushed.set()
            if hold_open:
                release.wait(4)
            self.close_connection = True

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    thread = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.02})
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/mcp", flushed, release
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        thread.join(1)


def sse(message, newline="\n", multiline=False):
    serialized = json.dumps(message, ensure_ascii=False, indent=2 if multiline else None)
    return (newline.join("data: " + line for line in serialized.split("\n")) + newline * 2).encode()


class ParallelSearchStreamingTests(unittest.TestCase):
    def rpc_over_http(self, body, media_type="text/event-stream", *, hold_open=True,
                      content_length=False, expected_error=None):
        done = Event()
        outcome, responses = [], []
        with http_fixture(body, media_type, hold_open=hold_open,
                          content_length=content_length) as (endpoint, flushed, release):
            client = ParallelSearch(timeout=3)
            client.ENDPOINT = endpoint

            def call():
                try:
                    with requests.Session() as session:
                        # Only this loopback fixture bypasses the sandbox proxy.
                        session.trust_env = False
                        session.hooks["response"].append(lambda response, **kw: responses.append(response))
                        outcome.append(client._rpc(session, "tools/call", 3, {}))
                except Exception as exc:
                    outcome.append(exc)
                finally:
                    done.set()

            worker = Thread(target=call, daemon=True)
            worker.start()
            try:
                self.assertTrue(flushed.wait(1), "Fixture did not flush a response")
                returned_while_open = done.wait(0.8)
            finally:
                release.set()
                worker.join(4)
            self.assertFalse(worker.is_alive(), "RPC worker exceeded its deadline")
            self.assertTrue(returned_while_open, "Client waited for EOF after a full RPC event")
        self.assertTrue(responses and responses[0].raw.closed, "RPC response was not closed")
        if expected_error:
            self.assertIsInstance(outcome[0], ParallelSearchError)
            self.assertIn(expected_error, str(outcome[0]))
        else:
            self.assertEqual(outcome, [RESULT])

    def test_open_sse_result_returns_and_closes_with_cr_lf_boundaries(self):
        for newline in ["\n", "\r\n", "\r"]:
            with self.subTest(newline=repr(newline)):
                # Notifications and other request IDs must not hide the matching result.
                prefix = b': heartbeat\r\n\r\n' + sse({"method": "notifications/progress"})
                prefix += sse({"id": 99, "result": {}}, "\r")
                body = prefix + sse({"id": 3, "result": RESULT}, newline, multiline=True)
                self.rpc_over_http(body)

    def test_open_sse_error_returns_and_closes(self):
        self.rpc_over_http(sse({"id": 3, "error": {"message": PASSAGE}}, "\r"),
                           expected_error="RPC error")

    def test_mixed_case_sse_media_type_on_open_and_closed_streams(self):
        for hold_open in [False, True]:
            with self.subTest(hold_open=hold_open):
                self.rpc_over_http(sse({"id": 3, "result": RESULT}),
                                   "Text/Event-Stream ; Charset=UTF-8", hold_open=hold_open)

    def test_json_media_type_with_parameters_keeps_working(self):
        self.rpc_over_http(json.dumps({"id": 3, "result": RESULT}, ensure_ascii=False).encode(),
                           "Application/JSON ; charset=UTF-8", content_length=True)


if __name__ == "__main__":
    unittest.main()
