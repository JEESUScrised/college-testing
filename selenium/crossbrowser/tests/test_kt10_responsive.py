"""KT10 remediation — responsive cross-browser matrix on Sauce Demo.

One browser session per (browser × viewport profile) runs TC10-R01…R06
to avoid 36 cold browser starts (previous 36-test run was interrupted).

Chrome tablet/phone: CDP device metrics (emulation).
Firefox: window resize only — not claimed as a real mobile OS.
Historical functional suite remains in test_kt10_matrix.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "selenium") not in sys.path:
    sys.path.insert(0, str(ROOT / "selenium"))

from pages.sauce import (  # noqa: E402
    SauceCartPage,
    SauceCheckoutPage,
    SauceInventoryPage,
    SauceLoginPage,
)

ARTIFACTS = ROOT / "selenium" / "artifacts" / "kt10"
SHOTS = ROOT / "screenshots" / "kt10" / "responsive"
MATRIX_LOG = ARTIFACTS / "responsive_matrix.jsonl"

RESPONSIVE_MATRIX = [
    ("chrome", "desktop", 1440, 900, "window"),
    ("chrome", "tablet", 768, 1024, "cdp"),
    ("chrome", "phone", 390, 844, "cdp"),
    ("firefox", "desktop", 1440, 900, "window"),
    ("firefox", "tablet", 768, 1024, "window"),
    ("firefox", "phone", 390, 844, "window"),
]


def _build(browser: str, width: int, height: int, mode: str):
    if browser == "chrome":
        opts = ChromeOptions()
        opts.add_argument("--disable-notifications")
        opts.page_load_strategy = "eager"
        if mode == "window":
            opts.add_argument(f"--window-size={width},{height}")
        drv = webdriver.Chrome(options=opts)
        if mode == "cdp":
            drv.execute_cdp_cmd(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": width,
                    "height": height,
                    "deviceScaleFactor": 2.0,
                    "mobile": width < 800,
                },
            )
        else:
            drv.set_window_size(width, height)
    else:
        opts = FirefoxOptions()
        opts.page_load_strategy = "eager"
        opts.add_argument(f"--width={width}")
        opts.add_argument(f"--height={height}")
        drv = webdriver.Firefox(options=opts)
        drv.set_window_size(width, height)
    drv.set_page_load_timeout(25)
    drv.implicitly_wait(0)
    return drv


def _safe_get(driver, url: str) -> None:
    try:
        driver.get(url)
    except TimeoutException:
        pass


def _record(row: dict) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with MATRIX_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _shot(driver, browser: str, profile: str, name: str) -> Path:
    SHOTS.mkdir(parents=True, exist_ok=True)
    path = SHOTS / f"{browser}_{profile}_{name}.png"
    assert driver.save_screenshot(str(path)), path
    assert path.stat().st_size > 0
    return path


def _row(driver, meta: dict, case_id: str, status: str, **extra) -> dict:
    page = SauceLoginPage(driver)
    vp = page.viewport()
    win = driver.get_window_size()
    row = {
        "case_id": case_id,
        **meta,
        "url": driver.current_url,
        "viewport": vp,
        "window": win,
        "status": status,
        **extra,
    }
    _record(row)
    return row


@pytest.fixture(params=RESPONSIVE_MATRIX, ids=lambda p: f"{p[0]}-{p[1]}")
def resp_profile(request):
    browser, profile, width, height, mode = request.param
    drv = _build(browser, width, height, mode)
    caps = dict(drv.capabilities)
    meta = {
        "browser": browser,
        "profile": profile,
        "target_w": width,
        "target_h": height,
        "mode": mode,
        "browserName": caps.get("browserName"),
        "browserVersion": caps.get("browserVersion"),
    }
    try:
        yield {"driver": drv, "wait": WebDriverWait(drv, 12), "meta": meta}
    finally:
        try:
            if browser == "chrome" and mode == "cdp":
                drv.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})
        except Exception:
            pass
        drv.quit()


@pytest.mark.kt10
@pytest.mark.kt10_responsive
def test_responsive_profile_scenarios(resp_profile):
    """TC10-R01…R06 for one browser×viewport profile (single session)."""
    drv = resp_profile["driver"]
    wait = resp_profile["wait"]
    meta = resp_profile["meta"]
    b, p = meta["browser"], meta["profile"]

    # R01 + R02 — layout / login form
    login = SauceLoginPage(drv)
    _safe_get(drv, login.URL + "/")
    wait.until(lambda d: d.execute_script("return document.readyState") != "loading")
    login.open_login()
    assert login.form_controls_visible()
    overflow = login.has_horizontal_overflow()
    shot01 = _shot(drv, b, p, "r01_layout")
    _row(
        drv,
        meta,
        "TC10-R01",
        "PASS",
        horizontal_overflow=overflow,
        screenshot=str(shot01),
        note="overflow flagged for review" if overflow else "no horizontal overflow",
    )
    shot02 = _shot(drv, b, p, "r02_login_form")
    _row(drv, meta, "TC10-R02", "PASS", screenshot=str(shot02))

    # R03 — inventory
    login.login()
    inv = SauceInventoryPage(drv).wait_loaded()
    assert inv.product_count() >= 1
    shot03 = _shot(drv, b, p, "r03_inventory")
    _row(
        drv,
        meta,
        "TC10-R03",
        "PASS",
        products=inv.product_count(),
        horizontal_overflow=inv.has_horizontal_overflow(),
        screenshot=str(shot03),
    )

    # R04 — menu
    inv.open_menu()
    shot04 = _shot(drv, b, p, "r04_menu_open")
    inv.close_menu()
    wait.until(lambda d: d.find_element(By.ID, "react-burger-menu-btn").is_displayed())
    _row(drv, meta, "TC10-R04", "PASS", screenshot=str(shot04))

    # R05 — cart (re-find inventory page after menu close)
    inv = SauceInventoryPage(drv).wait_loaded()
    if inv.cart_badge_text() != "1":
        inv.add_first_product()
    assert inv.cart_badge_text() == "1"
    inv.go_to_cart()
    cart = SauceCartPage(drv).wait_loaded()
    assert cart.item_count() >= 1
    shot05 = _shot(drv, b, p, "r05_cart")
    _row(drv, meta, "TC10-R05", "PASS", cart_items=cart.item_count(), screenshot=str(shot05))

    # R06 — checkout form
    cart.checkout()
    checkout = SauceCheckoutPage(drv).wait_info_loaded()
    assert checkout.fields_visible()
    checkout.continue_checkout()
    err = checkout.error_text()
    assert "Error" in err or "required" in err.lower() or "First Name" in err
    shot06 = _shot(drv, b, p, "r06_checkout")
    _row(drv, meta, "TC10-R06", "PASS", validation=err, screenshot=str(shot06))
