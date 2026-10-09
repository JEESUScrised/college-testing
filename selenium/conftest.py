"""Shared pytest fixtures for Selenium KT assignments."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_ROOT = PROJECT_ROOT / "screenshots"
FIXTURES_ROOT = Path(__file__).resolve().parent / "fixtures"
GRID_ROOT = Path(__file__).resolve().parent / "grid"
LOCAL_CHROMEDRIVER = Path(__file__).resolve().parent / "drivers" / "chromedriver.exe"
DEFAULT_PAGE_LOAD_TIMEOUT = 30
DEFAULT_IMPLICIT_WAIT = 5
DEFAULT_SCRIPT_TIMEOUT = 30
DEFAULT_EXPLICIT_WAIT = 10
DEFAULT_GRID_URL = os.environ.get("SELENIUM_GRID_URL", "http://127.0.0.1:4444")

# Allow importing selenium.grid helpers when running from repo root.
if str(GRID_ROOT) not in sys.path:
    sys.path.insert(0, str(GRID_ROOT))


def resolve_chrome_service() -> ChromeService | None:
    """Use a pre-cached ChromeDriver when available (offline KT05 workflow)."""
    candidates: list[Path] = []
    env_path = os.environ.get("SELENIUM_CHROMEDRIVER", "").strip()
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(LOCAL_CHROMEDRIVER)
    for path in candidates:
        if path.is_file():
            return ChromeService(executable_path=str(path.resolve()))
    return None



def fixture_file_url(*parts: str) -> str:
    """Return a file:// URL for an HTML fixture under selenium/fixtures/."""
    path = FIXTURES_ROOT.joinpath(*parts).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Fixture not found: {path}")
    return path.as_uri()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Browser for WebDriver tests (default: chrome)",
    )
    parser.addoption(
        "--page-load-strategy",
        action="store",
        default="normal",
        choices=("normal", "eager", "none"),
        help="Chrome/Firefox pageLoadStrategy (use 'none' for heavy sites like vdnh.ru)",
    )
    parser.addoption(
        "--grid-url",
        action="store",
        default=DEFAULT_GRID_URL,
        help="Selenium Grid hub/standalone URL (default: http://127.0.0.1:4444)",
    )


@pytest.fixture(scope="session")
def browser_name(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption("--browser")


@pytest.fixture(scope="session")
def page_load_strategy(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption("--page-load-strategy")


@pytest.fixture
def driver(browser_name: str, page_load_strategy: str):
    """Create a reusable WebDriver with sensible timeouts."""
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1400,1000")
        options.add_argument("--disable-notifications")
        options.page_load_strategy = page_load_strategy
        if page_load_strategy == "none":
            options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_service = resolve_chrome_service()
        drv = (
            webdriver.Chrome(options=options, service=chrome_service)
            if chrome_service is not None
            else webdriver.Chrome(options=options)
        )
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1400")
        options.add_argument("--height=1000")
        options.page_load_strategy = page_load_strategy
        drv = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError(f"Unsupported browser: {browser_name}")

    # Heavy public sites may never reach full network idle; keep get() bounded.
    load_timeout = 20 if page_load_strategy == "none" else DEFAULT_PAGE_LOAD_TIMEOUT
    drv.set_page_load_timeout(load_timeout)
    drv.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
    drv.set_script_timeout(DEFAULT_SCRIPT_TIMEOUT)

    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def wait(driver) -> WebDriverWait:
    """Explicit wait helper shared by Selenium tests."""
    return WebDriverWait(driver, DEFAULT_EXPLICIT_WAIT)


@pytest.fixture
def fixture_url():
    """Build file:// URLs for HTML fixtures under selenium/fixtures/."""

    def _url(*parts: str) -> str:
        return fixture_file_url(*parts)

    return _url


@pytest.fixture
def save_screenshot(driver):
    """Save a PNG screenshot under screenshots/<kt>/."""

    def _save(kt: str, name: str) -> Path:
        target_dir = SCREENSHOTS_ROOT / kt
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{name}.png"
        assert driver.save_screenshot(str(path)), f"Failed to save screenshot: {path}"
        return path

    return _save


@pytest.fixture(scope="session")
def grid_url(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption("--grid-url").rstrip("/")


@pytest.fixture(scope="session")
def fixture_http_server():
    """Serve selenium/fixtures over HTTP for remote Grid browsers."""
    from http_fixture_server import FixtureHttpServer

    server = FixtureHttpServer(FIXTURES_ROOT, host="127.0.0.1", port=0).start()
    try:
        yield server
    finally:
        server.stop()


@pytest.fixture(scope="session")
def fixture_http_url(fixture_http_server):
    """Build http://127.0.0.1:<port>/... URLs for fixtures (Grid-safe)."""

    def _url(*parts: str) -> str:
        return fixture_http_server.url(*parts)

    return _url


@pytest.fixture
def grid_driver(browser_name: str, page_load_strategy: str, grid_url: str, request):
    """Remote WebDriver session via Selenium Grid 4 (does not replace local `driver`)."""
    if browser_name != "chrome":
        pytest.skip("KT07 Grid demo on this PC uses Chrome only (Firefox/Edge not installed)")

    options = ChromeOptions()
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--disable-notifications")
    options.page_load_strategy = page_load_strategy
    # Visible name in Grid UI / session metadata
    options.set_capability("se:name", f"KT07:{request.node.name}")
    options.set_capability("se:kt", "07")

    drv: RemoteWebDriver = webdriver.Remote(command_executor=grid_url, options=options)
    # Prove this is RemoteWebDriver, not local Chrome()
    assert isinstance(drv, RemoteWebDriver), type(drv)
    assert not isinstance(drv, webdriver.Chrome)

    load_timeout = 20 if page_load_strategy == "none" else DEFAULT_PAGE_LOAD_TIMEOUT
    drv.set_page_load_timeout(load_timeout)
    drv.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
    drv.set_script_timeout(DEFAULT_SCRIPT_TIMEOUT)

    caps_path = PROJECT_ROOT / "selenium" / "artifacts" / "kt07"
    caps_path.mkdir(parents=True, exist_ok=True)
    session_meta = {
        "test": request.node.name,
        "session_id": drv.session_id,
        "command_executor": grid_url,
        "capabilities": dict(drv.capabilities),
    }
    meta_file = caps_path / f"session_{request.node.name}_{drv.session_id[:8]}.json"
    meta_file.write_text(json.dumps(session_meta, ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def grid_wait(grid_driver) -> WebDriverWait:
    return WebDriverWait(grid_driver, DEFAULT_EXPLICIT_WAIT)


@pytest.fixture
def save_grid_screenshot(grid_driver):
    """Save PNG screenshots from a Grid remote session under screenshots/kt07/."""

    def _save(name: str) -> Path:
        target_dir = SCREENSHOTS_ROOT / "kt07"
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{name}.png"
        assert grid_driver.save_screenshot(str(path)), f"Failed to save screenshot: {path}"
        return path

    return _save
