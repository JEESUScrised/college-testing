"""Capture readable Android Chrome SauceDemo screenshots for KT09.

Uses ChromeDriver web screenshots (nativeWebScreenshot=false) to avoid
emulator GPU compositor corruption, and disables password-manager prompts.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots" / "kt09" / "automated" / "android"
CHROMEDRIVER = ROOT / "mobile" / "drivers" / "chromedriver-134.exe"
BASE = "https://www.saucedemo.com"
UDID = "emulator-5554"
APPIUM = "http://127.0.0.1:4723"


def _adb(*args: str) -> None:
    subprocess.run(["adb", "-s", UDID, *args], check=False, capture_output=True)


def _prepare_device() -> None:
    _adb("shell", "am", "force-stop", "com.android.chrome")
    _adb("shell", "settings", "put", "secure", "autofill_service", "null")
    time.sleep(1.0)


def _dismiss_pw(drv) -> None:
    try:
        current = drv.current_context
        drv.switch_to.context("NATIVE_APP")
        time.sleep(0.2)
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
                time.sleep(0.3)
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


def _shot(drv, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.png"
    _dismiss_pw(drv)
    time.sleep(0.35)
    assert drv.get_screenshot_as_file(str(path)), path
    assert path.stat().st_size > 8_000, path
    print(f"  {name} {path.stat().st_size}")
    return path


def _wait(drv, css: str, timeout: int = 25):
    return WebDriverWait(drv, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))


def main() -> None:
    if not CHROMEDRIVER.is_file():
        raise SystemExit(f"Missing ChromeDriver: {CHROMEDRIVER}")

    _prepare_device()

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"
    options.browser_name = "Chrome"
    options.udid = UDID
    options.new_command_timeout = 240
    options.set_capability("appium:chromedriverExecutable", str(CHROMEDRIVER.resolve()))
    options.set_capability("appium:autoGrantPermissions", True)
    # Web screenshot = page canvas via ChromeDriver (readable; no GPU glitch overlay).
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
            ],
        },
    )

    drv = webdriver.Remote(APPIUM, options=options)
    paths: list[Path] = []
    try:
        try:
            web = next(
                (c for c in drv.contexts if "WEBVIEW" in c.upper() or "CHROMIUM" in c.upper()),
                None,
            )
            if web:
                drv.switch_to.context(web)
        except Exception:
            pass

        wait = WebDriverWait(drv, 30)
        drv.get(BASE + "/")
        try:
            drv.execute_script("try{localStorage.clear();sessionStorage.clear();}catch(e){}")
            drv.delete_all_cookies()
        except Exception:
            pass
        drv.get(BASE + "/")
        _wait(drv, "#user-name")
        paths.append(_shot(drv, "01_login"))

        drv.find_element(By.CSS_SELECTOR, "#user-name").clear()
        drv.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        drv.find_element(By.CSS_SELECTOR, "#password").clear()
        drv.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        drv.find_element(By.CSS_SELECTOR, "#login-button").click()
        _wait(drv, ".inventory_item_name")
        time.sleep(0.8)
        _dismiss_pw(drv)
        _wait(drv, ".inventory_item_name")
        paths.append(_shot(drv, "02_inventory"))

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item_name"))).click()
        _wait(drv, ".inventory_details_name")
        paths.append(_shot(drv, "03_product_details"))

        add = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory")))
        drv.execute_script("arguments[0].click();", add)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
        paths.append(_shot(drv, "04_added_to_cart"))

        drv.execute_script(
            "arguments[0].click();",
            drv.find_element(By.CSS_SELECTOR, ".shopping_cart_link"),
        )
        wait.until(EC.url_contains("cart.html"))
        _wait(drv, ".cart_item")
        paths.append(_shot(drv, "05_cart"))

        drv.get(BASE + "/inventory.html")
        _wait(drv, ".inventory_item")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-burger-menu-btn"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#logout_sidebar_link")))
        paths.append(_shot(drv, "06_menu"))

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-burger-cross-btn"))).click()
        time.sleep(0.3)
        # Ensure one cart item for checkout
        drv.get(BASE + "/inventory.html")
        _wait(drv, "button.btn_inventory")
        badge = drv.find_elements(By.CSS_SELECTOR, ".shopping_cart_badge")
        if not badge:
            drv.execute_script(
                "arguments[0].click();",
                drv.find_element(By.CSS_SELECTOR, "button.btn_inventory"),
            )
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
        drv.get(BASE + "/cart.html")
        _wait(drv, ".cart_item")
        drv.find_element(By.CSS_SELECTOR, "#checkout").click()
        wait.until(EC.url_contains("checkout-step-one"))
        _wait(drv, "#first-name")
        paths.append(_shot(drv, "07_checkout_form"))

        drv.find_element(By.CSS_SELECTOR, "#first-name").send_keys("QA")
        drv.find_element(By.CSS_SELECTOR, "#last-name").send_keys("Tester")
        drv.find_element(By.CSS_SELECTOR, "#postal-code").send_keys("12345")
        drv.find_element(By.CSS_SELECTOR, "#continue").click()
        wait.until(EC.url_contains("checkout-step-two"))
        drv.execute_script(
            "arguments[0].click();",
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#finish"))),
        )
        wait.until(EC.url_contains("checkout-complete"))
        _wait(drv, ".complete-header")
        paths.append(_shot(drv, "08_order_confirmation"))
    finally:
        drv.quit()

    print(f"DONE android shots={len(paths)}")
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
