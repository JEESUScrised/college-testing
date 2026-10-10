"""Local HTTP server for KT11 Robot fixtures (Suite Setup/Teardown)."""

from __future__ import annotations

import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from robot.api.deco import keyword, library

_FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
_httpd: ThreadingHTTPServer | None = None
_thread: threading.Thread | None = None
_base_url = ""


@library(scope="GLOBAL", auto_keywords=False)
class FixtureServer:
    """Start/stop a ThreadingHTTPServer serving robot/fixtures."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    @keyword("Start Fixture Server")
    def start_fixture_server(self) -> str:
        global _httpd, _thread, _base_url
        if _httpd is not None:
            return _base_url
        handler = functools.partial(
            SimpleHTTPRequestHandler, directory=str(_FIXTURES.resolve())
        )
        _httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        port = int(_httpd.server_address[1])
        _base_url = f"http://127.0.0.1:{port}"
        _thread = threading.Thread(target=_httpd.serve_forever, daemon=True)
        _thread.start()
        return _base_url

    @keyword("Stop Fixture Server")
    def stop_fixture_server(self) -> None:
        global _httpd, _thread, _base_url
        if _httpd is None:
            return
        _httpd.shutdown()
        _httpd.server_close()
        if _thread and _thread.is_alive():
            _thread.join(timeout=5)
        _httpd = None
        _thread = None
        _base_url = ""

    @keyword("Get Fixture Base URL")
    def get_fixture_base_url(self) -> str:
        if not _base_url:
            raise RuntimeError("Fixture server is not running")
        return _base_url
