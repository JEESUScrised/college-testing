"""Capture genuine KT09 SauceDemo screenshots (Windows Firefox + Android Chrome).

Android uses Appium webview screenshots with Chrome --disable-gpu to avoid
emulator compositor corruption. Windows uses Firefox (readable full UI).
"""

from __future__ import annotations

import time
from pathlib import Path

from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
ANDROID_OUT = ROOT / "screenshots" / "kt09" / "automated" / "android"
WINDOWS_OUT = ROOT / "screenshots" / "kt09" / "automated" / "windows"
CHROMEDRIVER = ROOT / "mobile" / "drivers" / "chromedriver-134.exe"
BASE = "https://www.saucedemo.com"
UDID = "emulator-5554"
APPIUM = "http://127.0.0.1:4723"


def _wait(drv, css: str, timeout: int = 25):
    return WebDriverWait(drv, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))


def _shot(drv, out: Path, name: str) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    assert drv.get_screenshot_as_file(str(path)), path
    assert path.stat().st_size > 15_000, path
    return path


def _dismiss_pw(drv) -> None:
    try:
        current = drv.current_context
        drv.switch_to.context("NATIVE_APP")
        time.sleep(0.25)
        for xpath in ('//*[@text="OK"]', '//*[@text="Ok"]', '//*[@resource-id="android:id/button1"]'):
            els = drv.find_elements(By.XPATH, xpath)
            if els:
                els[0].click()
                time.sleep(0.35)
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


def capture_android() -> list[Path]:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"
    options.browser_name = "Chrome"
    options.udid = UDID
    options.new_command_timeout = 180
    options.set_capability("appium:chromedriverExecutable", str(CHROMEDRIVER.resolve()))
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:nativeWebScreenshot", True)
    options.set_capability(
        "appium:chromeOptions",
        {
            "args": [
                "--disable-fre",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-gpu",
            ]
        },
    )

    drv = appium_webdriver.Remote(APPIUM, options=options)
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

        wait = WebDriverWait(drv, 25)
        drv.get(BASE + "/")
        try:
            drv.execute_script("try{localStorage.clear();sessionStorage.clear();}catch(e){}")
            drv.delete_all_cookies()
        except Exception:
            pass
        drv.get(BASE + "/")
        _wait(drv, "#user-name")
        time.sleep(0.7)
        _dismiss_pw(drv)
        _wait(drv, "#user-name")
        paths.append(_shot(drv, ANDROID_OUT, "01_login"))

        drv.find_element(By.CSS_SELECTOR, "#user-name").clear()
        drv.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        drv.find_element(By.CSS_SELECTOR, "#password").clear()
        drv.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        drv.find_element(By.CSS_SELECTOR, "#login-button").click()
        _wait(drv, ".inventory_item")
        time.sleep(0.7)
        _dismiss_pw(drv)
        _wait(drv, ".inventory_item_name")
        paths.append(_shot(drv, ANDROID_OUT, "02_inventory"))

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item_name"))).click()
        _wait(drv, ".inventory_details_name")
        time.sleep(0.5)
        _dismiss_pw(drv)
        paths.append(_shot(drv, ANDROID_OUT, "03_product_details"))

        add = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory")))
        drv.execute_script("arguments[0].click();", add)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
        paths.append(_shot(drv, ANDROID_OUT, "04_added_to_cart"))

        drv.execute_script(
            "arguments[0].click();",
            drv.find_element(By.CSS_SELECTOR, ".shopping_cart_link"),
        )
        wait.until(EC.url_contains("cart.html"))
        _wait(drv, ".cart_item")
        _dismiss_pw(drv)
        paths.append(_shot(drv, ANDROID_OUT, "05_cart"))

        drv.get(BASE + "/inventory.html")
        _wait(drv, ".inventory_item")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-burger-menu-btn"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#logout_sidebar_link")))
        paths.append(_shot(drv, ANDROID_OUT, "06_menu"))

        # Ensure cart item then checkout
        drv.get(BASE + "/inventory.html")
        _wait(drv, "button.btn_inventory")
        # reset cart via localStorage then add one
        drv.execute_script("try{localStorage.clear();}catch(e){}")
        drv.get(BASE + "/inventory.html")
        # need re-login after clear
        if "inventory" not in (drv.current_url or ""):
            _wait(drv, "#user-name")
            drv.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
            drv.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
            drv.find_element(By.CSS_SELECTOR, "#login-button").click()
            _wait(drv, ".inventory_item")
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
        paths.append(_shot(drv, ANDROID_OUT, "07_checkout_form"))

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
        paths.append(_shot(drv, ANDROID_OUT, "08_order_confirmation"))
    finally:
        drv.quit()
    return paths


def capture_windows() -> list[Path]:
    opts = FirefoxOptions()
    opts.add_argument("-width=1280")
    opts.add_argument("-height=900")
    drv = selenium_webdriver.Firefox(options=opts)
    paths: list[Path] = []
    try:
        wait = WebDriverWait(drv, 25)
        drv.set_window_size(1280, 900)
        drv.get(BASE + "/")
        _wait(drv, "#user-name")
        paths.append(_shot(drv, WINDOWS_OUT, "01_login"))

        drv.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        drv.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        drv.find_element(By.CSS_SELECTOR, "#login-button").click()
        _wait(drv, ".inventory_item")
        paths.append(_shot(drv, WINDOWS_OUT, "02_inventory"))

        drv.find_element(By.CSS_SELECTOR, ".inventory_item_name").click()
        _wait(drv, ".inventory_details_name")
        paths.append(_shot(drv, WINDOWS_OUT, "03_product_details"))

        drv.find_element(By.CSS_SELECTOR, "button.btn_inventory").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
        paths.append(_shot(drv, WINDOWS_OUT, "04_added_to_cart"))

        drv.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
        wait.until(EC.url_contains("cart.html"))
        _wait(drv, ".cart_item")
        paths.append(_shot(drv, WINDOWS_OUT, "05_cart"))

        drv.get(BASE + "/inventory.html")
        _wait(drv, ".inventory_item")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-burger-menu-btn"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#logout_sidebar_link")))
        paths.append(_shot(drv, WINDOWS_OUT, "06_menu"))

        drv.get(BASE + "/cart.html")
        _wait(drv, ".cart_item")
        drv.find_element(By.CSS_SELECTOR, "#checkout").click()
        wait.until(EC.url_contains("checkout-step-one"))
        _wait(drv, "#first-name")
        paths.append(_shot(drv, WINDOWS_OUT, "07_checkout_form"))

        drv.find_element(By.CSS_SELECTOR, "#first-name").send_keys("QA")
        drv.find_element(By.CSS_SELECTOR, "#last-name").send_keys("Tester")
        drv.find_element(By.CSS_SELECTOR, "#postal-code").send_keys("12345")
        drv.find_element(By.CSS_SELECTOR, "#continue").click()
        wait.until(EC.url_contains("checkout-step-two"))
        drv.find_element(By.CSS_SELECTOR, "#finish").click()
        wait.until(EC.url_contains("checkout-complete"))
        _wait(drv, ".complete-header")
        paths.append(_shot(drv, WINDOWS_OUT, "08_order_confirmation"))
    finally:
        drv.quit()
    return paths


def main() -> None:
    print("Capturing Android…")
    for p in capture_android():
        print(f"  ANDROID {p.name} {p.stat().st_size}")
    print("Capturing Windows Firefox…")
    for p in capture_windows():
        print(f"  WINDOWS {p.name} {p.stat().st_size}")
    print("DONE")


if __name__ == "__main__":
    main()
