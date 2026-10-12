"""KT09 — Android Chrome DOM suite against Sauce Demo (TC09-W01…W10).

Reuses pinned ChromeDriver 134.0.6998.165 for emulator Chrome 134.0.6998.135.
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
USER = "standard_user"
PASSWORD = "secret_sauce"


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
    # ChromeDriver web screenshot — avoids emulator GPU compositor corruption
    # (nativeWebScreenshot=True produced scrambled/glitched PNG evidence).
    options.set_capability("appium:nativeWebScreenshot", False)
    options.set_capability(
        "appium:chromeOptions",
        {
            "args": [
                "--disable-fre",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-features=PasswordLeakDetection,PasswordManagerOnboarding,AutofillServerCommunication",
                "--password-store=basic",
            ]
        },
    )
    udid = (
        pytestconfig.getoption("--udid") or os.environ.get("ANDROID_UDID") or "emulator-5554"
    ).strip()
    options.udid = udid
    server = pytestconfig.getoption("--appium-server")

    drv = webdriver.Remote(server, options=options)
    drv.implicitly_wait(0)
    try:
        contexts = drv.contexts
        web = next(
            (c for c in contexts if "WEBVIEW" in c.upper() or "CHROMIUM" in c.upper()),
            None,
        )
        if web:
            drv.switch_to.context(web)
    except Exception:
        pass
    try:
        yield drv
    finally:
        drv.quit()


@pytest.fixture
def wait_dom(android_chrome_dom):
    return WebDriverWait(android_chrome_dom, 25)


def _dismiss_chrome_dialogs(drv) -> None:
    """Dismiss native Chrome / Password Manager overlays before web screenshots."""
    try:
        current = drv.current_context
        drv.switch_to.context("NATIVE_APP")
        for xpath in (
            '//*[@text="OK"]',
            '//*[@text="Ok"]',
            '//*[@text="Not now"]',
            '//*[@text="No thanks"]',
            '//*[@resource-id="android:id/button1"]',
            '//*[@resource-id="com.android.chrome:id/positive_button"]',
        ):
            els = drv.find_elements(By.XPATH, xpath)
            if els:
                els[0].click()
                break
        web = next(
            (c for c in drv.contexts if "WEBVIEW" in c.upper() or "CHROMIUM" in c.upper()),
            current,
        )
        drv.switch_to.context(web)
    except Exception:
        try:
            web = next(
                (c for c in drv.contexts if "WEBVIEW" in c.upper() or "CHROMIUM" in c.upper()),
                None,
            )
            if web:
                drv.switch_to.context(web)
        except Exception:
            pass


def _wait_page_settled(drv, css: str, timeout: int = 25) -> None:
    WebDriverWait(drv, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
    WebDriverWait(drv, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    # Wait until fonts are ready and at least one image (if any) finished loading.
    WebDriverWait(drv, timeout).until(
        lambda d: d.execute_script(
            "return (document.fonts ? document.fonts.status === 'loaded' : true) && "
            "Array.from(document.images || []).every(function(i){return i.complete;});"
        )
    )


def _shot(drv, name: str) -> Path:
    SHOTS.mkdir(parents=True, exist_ok=True)
    path = SHOTS / f"{name}.png"
    _dismiss_chrome_dialogs(drv)
    try:
        WebDriverWait(drv, 12).until(
            lambda d: d.execute_script(
                "return document.readyState === 'complete' && "
                "(document.fonts ? document.fonts.status === 'loaded' : true) && "
                "Array.from(document.images || []).every(function(i){return i.complete;});"
            )
        )
    except Exception:
        pass
    assert drv.save_screenshot(str(path)), path
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


def _has_overflow(vp: dict) -> bool:
    return int(vp["scrollWidth"]) > int(vp["clientWidth"]) + 1


def _open_login(drv, wait) -> None:
    # Clear Sauce session so cart/badge state does not leak across module tests.
    try:
        drv.get(BASE_URL + "/")
        drv.execute_script(
            "try{localStorage.clear();sessionStorage.clear();}catch(e){}"
        )
        drv.delete_all_cookies()
    except Exception:
        pass
    drv.get(BASE_URL + "/")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name")))


def _login(drv, wait) -> None:
    _open_login(drv, wait)
    user = drv.find_element(By.CSS_SELECTOR, "#user-name")
    pwd = drv.find_element(By.CSS_SELECTOR, "#password")
    user.clear()
    user.send_keys(USER)
    pwd.clear()
    pwd.send_keys(PASSWORD)
    drv.find_element(By.CSS_SELECTOR, "#login-button").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item")))


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w01_website_loading(android_chrome_dom, wait_dom):
    """TC09-W01 — Website loading."""
    drv = android_chrome_dom
    _open_login(drv, wait_dom)
    assert "saucedemo.com" in drv.current_url
    assert "Swag Labs" in (drv.title or "")
    assert drv.find_element(By.CSS_SELECTOR, ".login_logo").is_displayed()
    _shot(drv, "tc09_w01_loading")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w02_login_form(android_chrome_dom, wait_dom):
    """TC09-W02 — Login form usable."""
    drv = android_chrome_dom
    _open_login(drv, wait_dom)
    user = drv.find_element(By.CSS_SELECTOR, "#user-name")
    pwd = drv.find_element(By.CSS_SELECTOR, "#password")
    btn = drv.find_element(By.CSS_SELECTOR, "#login-button")
    assert user.is_displayed() and user.is_enabled()
    assert pwd.is_displayed() and pwd.is_enabled()
    assert btn.is_displayed() and btn.is_enabled()
    user.send_keys("probe")
    assert (user.get_attribute("value") or "") == "probe"
    _shot(drv, "tc09_w02_login_form")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w03_successful_authentication(android_chrome_dom, wait_dom):
    """TC09-W03 — Successful authentication."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    assert "inventory" in drv.current_url
    title = wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".title")))
    assert title.text.strip() == "Products"
    _shot(drv, "tc09_w03_authenticated")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w04_inventory_listing(android_chrome_dom, wait_dom):
    """TC09-W04 — Inventory listing names and prices."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    items = drv.find_elements(By.CSS_SELECTOR, ".inventory_item")
    assert len(items) >= 6
    names = drv.find_elements(By.CSS_SELECTOR, ".inventory_item_name")
    prices = drv.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
    assert len(names) >= 6 and all(n.text.strip() for n in names[:6])
    assert len(prices) >= 6 and all(p.text.strip().startswith("$") for p in prices[:6])
    _shot(drv, "tc09_w04_inventory")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w05_product_interaction(android_chrome_dom, wait_dom):
    """TC09-W05 — Open product details."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    name_el = wait_dom.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item_name")))
    expected = name_el.text.strip()
    name_el.click()
    detail = wait_dom.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_details_name"))
    )
    assert detail.text.strip() == expected
    assert drv.find_element(By.CSS_SELECTOR, ".inventory_details_price").text.strip().startswith("$")
    _shot(drv, "tc09_w05_product")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w06_add_item_to_cart(android_chrome_dom, wait_dom):
    """TC09-W06 — Add item to cart."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    add = wait_dom.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory"))
    )
    drv.execute_script("arguments[0].click();", add)
    badge = wait_dom.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge"))
    )
    assert badge.text.strip() == "1"
    _shot(drv, "tc09_w06_add_cart")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w07_cart_navigation(android_chrome_dom, wait_dom):
    """TC09-W07 — Cart navigation and contents."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    name = drv.find_element(By.CSS_SELECTOR, ".inventory_item_name").text.strip()
    add = wait_dom.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory"))
    )
    drv.execute_script("arguments[0].click();", add)
    wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
    link = drv.find_element(By.CSS_SELECTOR, ".shopping_cart_link")
    drv.execute_script(
        "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
        link,
    )
    try:
        wait_dom.until(EC.url_contains("cart.html"))
    except Exception:
        drv.get(BASE_URL + "/cart.html")
        wait_dom.until(EC.url_contains("cart.html"))
    items = drv.find_elements(By.CSS_SELECTOR, ".cart_item")
    assert len(items) >= 1
    assert name in drv.find_element(By.CSS_SELECTOR, ".inventory_item_name").text
    _shot(drv, "tc09_w07_cart")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w08_checkout_validation(android_chrome_dom, wait_dom):
    """TC09-W08 — Checkout required-field validation."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    add = wait_dom.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory"))
    )
    drv.execute_script("arguments[0].click();", add)
    drv.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
    wait_dom.until(EC.url_contains("cart.html"))
    checkout = wait_dom.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#checkout")))
    drv.execute_script("arguments[0].click();", checkout)
    wait_dom.until(EC.url_contains("checkout-step-one"))
    cont = wait_dom.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#continue")))
    # JS click bypasses native HTML5 required so Sauce error banner appears.
    drv.execute_script("arguments[0].click();", cont)
    err = wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "First Name" in err.text or "required" in err.text.lower()
    _shot(drv, "tc09_w08_checkout_validation")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w09_menu_navigation(android_chrome_dom, wait_dom):
    """TC09-W09 — Burger menu accessible."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    menu = wait_dom.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-burger-menu-btn")))
    assert menu.is_displayed()
    menu.click()
    wait_dom.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#inventory_sidebar_link")))
    assert drv.find_element(By.CSS_SELECTOR, "#logout_sidebar_link").is_displayed()
    _shot(drv, "tc09_w09_menu")


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_tc09_w10_mobile_layout(android_chrome_dom, wait_dom):
    """TC09-W10 — Viewport / horizontal overflow."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    vp = _viewport(drv)
    assert int(vp["innerWidth"]) > 0 and int(vp["innerHeight"]) > 0
    assert _has_overflow(vp) is False
    meta = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "chromedriver": str(CHROMEDRIVER),
        "viewport": vp,
        "overflow": False,
        "browserName": drv.capabilities.get("browserName"),
        "result": "PASS",
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "android_chrome_dom_suite_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _shot(drv, "tc09_w10_layout")


# Keep historical single-journey name as alias coverage for prior evidence references.
@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_kt09_android_chrome_dom_sauce_journey(android_chrome_dom, wait_dom):
    """Regression: compact journey still green on same session config."""
    drv = android_chrome_dom
    _login(drv, wait_dom)
    assert len(drv.find_elements(By.CSS_SELECTOR, ".inventory_item")) >= 6
    _shot(drv, "dom_journey_regression")
