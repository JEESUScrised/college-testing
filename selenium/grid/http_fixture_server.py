"""Tiny HTTP server that serves selenium/fixtures for remote Grid browsers.

Remote WebDriver sessions cannot rely on file:// paths from the pytest client
machine when the browser runs in a Grid node process (even on localhost it is
cleaner and more realistic to use HTTP).
"""

from __future__ import annotations

import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class FixtureHttpServer:
    def __init__(self, directory: Path, host: str = "127.0.0.1", port: int = 0) -> None:
        self.directory = directory.resolve()
        handler = functools.partial(SimpleHTTPRequestHandler, directory=str(self.directory))
        self._httpd = ThreadingHTTPServer((host, port), handler)
        self.host = host
        self.port = self._httpd.server_address[1]
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def start(self) -> "FixtureHttpServer":
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)

    def url(self, *parts: str) -> str:
        rel = "/".join(parts)
        return f"{self.base_url}/{rel}"
