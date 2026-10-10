"""Local HTTP server for KT10 fixtures (Grid/browser-safe URLs)."""

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
        self.port = int(self._httpd.server_address[1])
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
        return f"{self.base_url}/{'/'.join(parts)}"
