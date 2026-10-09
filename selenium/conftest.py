"""Shared pytest fixtures for Selenium KT assignments."""

from __future__ import annotations

from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_ROOT = PROJECT_ROOT / "screenshots"
DEFAULT_PAGE_LOAD_TIMEOUT = 30
DEFAULT_IMPLICIT_WAIT = 5
DEFAULT_SCRIPT_TIMEOUT = 30


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Browser for WebDriver tests (default: chrome)",
    )


@pytest.fixture(scope="session")
def browser_name(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption("--browser")


@pytest.fixture
def driver(browser_name: str):
    """Create a reusable WebDriver with sensible timeouts."""
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-notifications")
        drv = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1280")
        options.add_argument("--height=900")
        drv = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError(f"Unsupported browser: {browser_name}")

    drv.set_page_load_timeout(DEFAULT_PAGE_LOAD_TIMEOUT)
    drv.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
    drv.set_script_timeout(DEFAULT_SCRIPT_TIMEOUT)

    try:
        yield drv
    finally:
        drv.quit()


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
