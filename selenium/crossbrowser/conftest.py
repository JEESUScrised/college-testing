"""KT10 fixtures: dedicated driver + EventFiringWebDriver + HTTP fixtures.

Does not replace selenium/conftest.py `driver` used by KT01–KT08.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.support.ui import WebDriverWait

CROSSBROWSER_ROOT = Path(__file__).resolve().parent
SELENIUM_ROOT = CROSSBROWSER_ROOT.parent
PROJECT_ROOT = SELENIUM_ROOT.parent
FIXTURES_ROOT = SELENIUM_ROOT / "fixtures"
ARTIFACTS = PROJECT_ROOT / "selenium" / "artifacts" / "kt10"
SCREENSHOTS = PROJECT_ROOT / "screenshots" / "kt10"
VIEWPORT = (1400, 1000)

if str(CROSSBROWSER_ROOT) not in sys.path:
    sys.path.insert(0, str(CROSSBROWSER_ROOT))

from http_server import FixtureHttpServer  # noqa: E402
from listener import Kt10EventListener  # noqa: E402


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "kt10: KT10 cross-browser + listeners + reporting")
    config.addinivalue_line(
        "markers", "kt10_failure_demo: intentional failure for screenshot-on-failure demo"
    )
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def kt10_http():
    server = FixtureHttpServer(FIXTURES_ROOT, host="127.0.0.1", port=0).start()
    try:
        yield server
    finally:
        server.stop()


@pytest.fixture(scope="session")
def kt10_url(kt10_http):
    def _url(*parts: str) -> str:
        return kt10_http.url(*parts)

    return _url


def _build_driver(browser: str):
    browser = browser.lower()
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument(f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}")
        options.add_argument("--disable-notifications")
        drv = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument(f"--width={VIEWPORT[0]}")
        options.add_argument(f"--height={VIEWPORT[1]}")
        drv = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError(f"Unsupported KT10 browser: {browser}")
    drv.set_window_size(*VIEWPORT)
    drv.set_page_load_timeout(30)
    drv.implicitly_wait(0)
    drv.set_script_timeout(30)
    return drv


@pytest.fixture
def kt10_browser(request) -> str:
    """Browser for current KT10 parametrized test (chrome|firefox)."""
    return request.param


@pytest.fixture
def kt10_listener(kt10_browser, request) -> Kt10EventListener:
    test_id = request.node.name
    path = ARTIFACTS / "events.jsonl"
    return Kt10EventListener(path, browser_name=kt10_browser, test_id=test_id)


@pytest.fixture
def kt10_driver(kt10_browser: str, kt10_listener: Kt10EventListener, request):
    """Dedicated EventFiringWebDriver for KT10 (does not use shared `driver`)."""
    raw = _build_driver(kt10_browser)
    firing = EventFiringWebDriver(raw, kt10_listener)
    # Expose metadata for hooks/reporting
    request.node._kt10_browser = kt10_browser  # type: ignore[attr-defined]
    request.node._kt10_caps = dict(raw.capabilities)  # type: ignore[attr-defined]
    request.node._kt10_listener = kt10_listener  # type: ignore[attr-defined]
    try:
        yield firing
    finally:
        firing.quit()


@pytest.fixture
def kt10_wait(kt10_driver) -> WebDriverWait:
    return WebDriverWait(kt10_driver, 10)


@pytest.fixture
def kt10_shot(kt10_driver, kt10_browser):
    def _save(name: str) -> Path:
        path = SCREENSHOTS / f"{kt10_browser}_{name}.png"
        assert kt10_driver.save_screenshot(str(path)), path
        assert path.is_file() and path.stat().st_size > 0
        return path

    return _save


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook (separate from WebDriver listener): attach failure screenshots."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when != "call":
        return
    browser = getattr(item, "_kt10_browser", None) or "unknown"
    caps = getattr(item, "_kt10_caps", {}) or {}
    summary = {
        "test_id": item.nodeid,
        "browser": browser,
        "browserName": caps.get("browserName"),
        "browserVersion": caps.get("browserVersion"),
        "outcome": report.outcome,
        "duration_s": getattr(report, "duration", None),
        "longrepr": str(report.longrepr)[:1000] if report.failed else None,
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with (ARTIFACTS / "run_summary.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(summary, ensure_ascii=False) + "\n")

    if report.failed:
        driver = item.funcargs.get("kt10_driver")
        if driver is not None:
            shot = SCREENSHOTS / f"FAIL_{browser}_{item.name}.png"
            try:
                driver.save_screenshot(str(shot))
                summary["screenshot"] = str(shot)
                try:
                    from pytest_html import extras as html_extras

                    extra = list(getattr(report, "extras", []) or [])
                    extra.append(html_extras.png(str(shot)))
                    extra.append(html_extras.text(f"browser={browser}"))
                    report.extras = extra
                except Exception:
                    pass
            except Exception as exc:  # noqa: BLE001
                summary["screenshot_error"] = str(exc)
            with (ARTIFACTS / "failures.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(summary, ensure_ascii=False) + "\n")
