"""Selenium WebDriver event listener for KT10 (not pytest hooks)."""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener

_lock = threading.Lock()


class Kt10EventListener(AbstractEventListener):
    """Records navigation/click/exception events with timestamps."""

    def __init__(
        self,
        log_path: Path,
        *,
        browser_name: str = "",
        test_id: str = "",
    ) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.browser_name = browser_name
        self.test_id = test_id
        self.events: list[dict[str, Any]] = []

    def _record(self, kind: str, **payload: Any) -> None:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": kind,
            "browser": self.browser_name,
            "test_id": self.test_id,
            **payload,
        }
        self.events.append(entry)
        line = json.dumps(entry, ensure_ascii=False)
        with _lock:
            with self.log_path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")

    def before_navigate_to(self, url, driver) -> None:  # noqa: ANN001
        self._record("before_navigate_to", url=url)

    def after_navigate_to(self, url, driver) -> None:  # noqa: ANN001
        self._record("after_navigate_to", url=url, title=getattr(driver, "title", ""))

    def before_click(self, element, driver) -> None:  # noqa: ANN001
        self._record(
            "before_click",
            tag=getattr(element, "tag_name", None),
            text=(getattr(element, "text", "") or "")[:80],
            id=element.get_attribute("id") if element is not None else None,
        )

    def after_click(self, element, driver) -> None:  # noqa: ANN001
        self._record(
            "after_click",
            tag=getattr(element, "tag_name", None),
            id=element.get_attribute("id") if element is not None else None,
        )

    def on_exception(self, exception, driver) -> None:  # noqa: ANN001
        self._record(
            "on_exception",
            error_type=type(exception).__name__,
            error=str(exception)[:500],
        )
