"""Shared fixtures for KT06/KT09 Appium Android tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

MOBILE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = MOBILE_ROOT.parent
APK_PATH = MOBILE_ROOT / "apps" / "ApiDemos-debug.apk"
SCREENSHOTS_ROOT = PROJECT_ROOT / "screenshots"
DEFAULT_APPIUM_URL = os.environ.get("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
DEFAULT_EXPLICIT_WAIT = 15


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--appium-server",
        action="store",
        default=DEFAULT_APPIUM_URL,
        help="Appium server URL (default: http://127.0.0.1:4723)",
    )
    parser.addoption(
        "--device-name",
        action="store",
        default=os.environ.get("ANDROID_DEVICE_NAME", "Android Emulator"),
        help="deviceName capability",
    )
    parser.addoption(
        "--udid",
        action="store",
        default=os.environ.get("ANDROID_UDID", ""),
        help="Optional device udid from adb devices",
    )


@pytest.fixture(scope="session")
def apk_path() -> Path:
    if not APK_PATH.is_file():
        raise pytest.UsageError(
            f"APK not found: {APK_PATH}. See mobile/apps/README.md"
        )
    return APK_PATH


@pytest.fixture(scope="session")
def appium_server(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption("--appium-server")


@pytest.fixture(scope="session")
def android_driver(apk_path: Path, appium_server: str, pytestconfig: pytest.Config):
    """One shared Android driver session for the whole KT06 module (no emulator restart)."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = pytestconfig.getoption("--device-name")
    options.app = str(apk_path.resolve())
    options.app_package = "io.appium.android.apis"
    options.app_activity = ".ApiDemos"
    options.no_reset = False
    options.new_command_timeout = 120
    options.set_capability("appium:autoGrantPermissions", True)

    udid = (pytestconfig.getoption("--udid") or "").strip()
    if udid:
        options.udid = udid

    driver: WebDriver = webdriver.Remote(appium_server, options=options)
    driver.implicitly_wait(0)
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def driver(android_driver: WebDriver):
    """Per-test alias that resets to the ApiDemos home activity."""
    android_driver.execute_script(
        "mobile: startActivity",
        {"component": "io.appium.android.apis/.ApiDemos"},
    )
    return android_driver


@pytest.fixture
def wait(driver: WebDriver) -> WebDriverWait:
    return WebDriverWait(driver, DEFAULT_EXPLICIT_WAIT)


@pytest.fixture
def save_screenshot(driver: WebDriver):
    def _save(kt: str, name: str) -> Path:
        target_dir = SCREENSHOTS_ROOT / kt
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{name}.png"
        assert driver.get_screenshot_as_file(str(path)), f"Failed screenshot: {path}"
        assert path.is_file() and path.stat().st_size > 0
        return path

    return _save
