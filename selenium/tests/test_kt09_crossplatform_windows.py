"""KT09 remediation — Windows desktop browsers vs public Sauce Demo."""

from __future__ import annotations

from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.sauce import SauceInventoryPage, SauceLoginPage
from pages.sauce.base import BASE_URL

SHOTS = Path(__file__).resolve().parents[2] / "screenshots" / "kt09" / "crossplatform"


@pytest.fixture(params=["chrome", "firefox"])
def xp_driver(request, page_load_strategy):
    browser = request.param
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-notifications")
        options.page_load_strategy = page_load_strategy
        drv = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.page_load_strategy = page_load_strategy
        drv = webdriver.Firefox(options=options)
    drv.set_page_load_timeout(25)
    try:
        drv.set_window_size(1280, 900)
    except Exception:
        pass
    try:
        drv.get(BASE_URL + "/")
    except TimeoutException:
        pass
    request.node._kt09_browser = browser  # type: ignore[attr-defined]
    try:
        yield drv
    finally:
        drv.quit()


def _shot(driver, browser: str, name: str) -> None:
    SHOTS.mkdir(parents=True, exist_ok=True)
    assert driver.save_screenshot(str(SHOTS / f"windows_{browser}_{name}.png"))


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_kt09_windows_sauce_login_inventory(xp_driver, request):
    """Public web smoke on Windows desktop browsers."""
    browser = request.node._kt09_browser  # type: ignore[attr-defined]
    login = SauceLoginPage(xp_driver).open_login()
    assert login.form_controls_visible()
    _shot(xp_driver, browser, "01_login")
    login.login()
    inv = SauceInventoryPage(xp_driver).wait_loaded()
    assert inv.product_count() >= 6
    _shot(xp_driver, browser, "02_inventory")
