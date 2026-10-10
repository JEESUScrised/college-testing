"""KT09 — Android Chrome DOM automation against Sauce Demo (real WebDriver).

Uses explicitly pinned host ChromeDriver matching emulator Chrome 134.x.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MOBILE_ROOT = Path(__file__).resolve().parents[1]
CHROMEDRIVER = MOBILE_ROOT / "drivers" / "chromedriver-134.exe"
SHOTS = PROJECT_ROOT / "screenshots" / "kt09" / "crossplatform" / "dom"
ARTIFACTS = MOBILE_ROOT / "artifacts" / "kt09"
BASE_URL = "https://www.saucedemo.com"
DEFAULT_APPIUM = os.environ.get("APPIUM_SERVER_URL", "http://127.0.0.1:4723")


@pytest.fixture(scope="module")
def android_chrome_dom(pytestconfig):
    if not CHROMEDRIVER.is_file():
        pytest.skip(f"Pinned ChromeDriver missing: {CHROMEDRIVER}")

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = pytestconfig.getoption("--device-name")
    options.browser_name = "Chrome"
    options.new_command_timeout = 180
    options.set_capability("appium:chromedriverExecutable", str(CHROMEDRIVER.resolve()))
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:nativeWebScreenshot", True)
    # Skip Chrome first-run / notification promos where supported
    options.set_capability(
        "appium:chromeOptions",
        {"args": ["--disable-fre", "--no-first-run", "--no-default-browser-check"]},
    )

    udid = (pytestconfig.getoption("--udid") or os.environ.get("ANDROID_UDID") or "emulator-5554").strip()
    options.udid = udid
    server = pytestconfig.getoption("--appium-server")

    drv = webdriver.Remote(server, options=options)
    drv.implicitly_wait(0)
    # Ensure WEBVIEW/CHROMIUM context for DOM locators (not NATIVE_APP).
    try:
        contexts = drv.contexts
        web = next((c for c in contexts if "WEBVIEW" in c.upper() or "CHROMIUM" in c.upper()), None)
        if web:
            drv.switch_to.context(web)
        elif "CHROMIUM" in contexts:
            drv.switch_to.context("CHROMIUM")
    except Exception:
        pass
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def wait_dom(android_chrome_dom):
    return WebDriverWait(android_chrome_dom, 25)


def _shot(drv, name: str) -> Path:
    SHOTS.mkdir(parents=True, exist_ok=True)
    path = SHOTS / f"{name}.png"
    assert drv.save_screenshot(str(path))
    return path


def _viewport(drv) -> dict:
    return drv.execute_script(
        "return {"
        "innerWidth: window.innerWidth,"
        "innerHeight: window.innerHeight,"
        "clientWidth: document.documentElement.clientWidth,"
        "scrollWidth: document.documentElement.scrollWidth,"
        "scrollHeight: document.documentElement.scrollHeight,"
        "devicePixelRatio: window.devicePixelRatio"
        "};"
    )


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_kt09_android_chrome_dom_sauce_journey(android_chrome_dom, wait_dom):
    """Full DOM journey: login → inventory → product → cart."""
    drv = android_chrome_dom
    evidence: dict = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "chromedriver": str(CHROMEDRIVER),
        "browserName": drv.capabilities.get("browserName"),
        "platform": drv.capabilities.get("platformName"),
        "device": drv.capabilities.get("deviceName") or drv.capabilities.get("appium:deviceName"),
    }

    drv.get(BASE_URL + "/")
    # CSS locators: Appium Chromium context rejects some By.ID mappings.
    user = wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name")))
    pwd = drv.find_element(By.CSS_SELECTOR, "#password")
    btn = drv.find_element(By.CSS_SELECTOR, "#login-button")
    assert user.is_displayed() and pwd.is_displayed() and btn.is_displayed()
    evidence["viewport_login"] = _viewport(drv)
    evidence["overflow_login"] = (
        int(evidence["viewport_login"]["scrollWidth"])
        > int(evidence["viewport_login"]["clientWidth"]) + 1
    )
    _shot(drv, "dom_01_login")

    user.clear()
    user.send_keys("standard_user")
    pwd.clear()
    pwd.send_keys("secret_sauce")
    btn.click()

    wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item")))
    items = drv.find_elements(By.CSS_SELECTOR, ".inventory_item")
    assert len(items) >= 6
    evidence["product_count"] = len(items)
    evidence["viewport_inventory"] = _viewport(drv)
    evidence["overflow_inventory"] = (
        int(evidence["viewport_inventory"]["scrollWidth"])
        > int(evidence["viewport_inventory"]["clientWidth"]) + 1
    )
    _shot(drv, "dom_02_inventory")

    # Open first product details
    name_el = wait_dom.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item_name")))
    product_name = name_el.text.strip()
    name_el.click()
    detail = wait_dom.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_details_name"))
    )
    assert detail.text.strip() == product_name
    _shot(drv, "dom_03_product")

    add = wait_dom.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory")))
    add.click()
    wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
    badge = drv.find_element(By.CSS_SELECTOR, ".shopping_cart_badge").text.strip()
    assert badge == "1"

    drv.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
    wait_dom.until(EC.url_contains("cart.html"))
    cart_items = drv.find_elements(By.CSS_SELECTOR, ".cart_item")
    assert len(cart_items) == 1
    cart_name = drv.find_element(By.CSS_SELECTOR, ".inventory_item_name").text.strip()
    assert cart_name == product_name
    _shot(drv, "dom_04_cart")

    # Burger menu accessible
    menu = wait_dom.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-burger-menu-btn")))
    assert menu.is_displayed()
    menu.click()
    wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#inventory_sidebar_link")))
    _shot(drv, "dom_05_menu")

    evidence["product_name"] = product_name
    evidence["cart_count"] = 1
    evidence["ended_utc"] = datetime.now(timezone.utc).isoformat()
    evidence["result"] = "PASS"
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "android_chrome_dom_evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )
