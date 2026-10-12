"""One-shot Android capture through order confirmation (proven DOM capabilities)."""

from __future__ import annotations

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


def main() -> None:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"
    options.browser_name = "Chrome"
    options.udid = "emulator-5554"
    options.new_command_timeout = 180
    options.set_capability("appium:chromedriverExecutable", str(CHROMEDRIVER.resolve()))
    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:nativeWebScreenshot", False)
    options.set_capability(
        "appium:chromeOptions",
        {
            "args": [
                "--disable-fre",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-features=PasswordLeakDetection,PasswordManagerOnboarding",
                "--password-store=basic",
            ]
        },
    )
    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)
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
        OUT.mkdir(parents=True, exist_ok=True)

        drv.get(BASE + "/")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name"))).send_keys(
            "standard_user"
        )
        drv.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
        drv.find_element(By.CSS_SELECTOR, "#login-button").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item")))
        # dismiss password dialog if any
        try:
            cur = drv.current_context
            drv.switch_to.context("NATIVE_APP")
            time.sleep(0.3)
            for xp in ('//*[@text="OK"]', '//*[@resource-id="android:id/button1"]'):
                els = drv.find_elements(By.XPATH, xp)
                if els:
                    els[0].click()
                    break
            web = next(
                (c for c in drv.contexts if "WEBVIEW" in c.upper() or "CHROMIUM" in c.upper()),
                cur,
            )
            drv.switch_to.context(web)
        except Exception:
            pass

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory")))
        drv.execute_script(
            "arguments[0].click();",
            drv.find_element(By.CSS_SELECTOR, "button.btn_inventory"),
        )
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
        drv.get(BASE + "/cart.html")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart_item")))
        drv.find_element(By.CSS_SELECTOR, "#checkout").click()
        wait.until(EC.url_contains("checkout-step-one"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#first-name"))).send_keys("QA")
        drv.find_element(By.CSS_SELECTOR, "#last-name").send_keys("Tester")
        drv.find_element(By.CSS_SELECTOR, "#postal-code").send_keys("12345")
        drv.find_element(By.CSS_SELECTOR, "#continue").click()
        wait.until(EC.url_contains("checkout-step-two"))
        drv.execute_script(
            "arguments[0].click();",
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#finish"))),
        )
        wait.until(EC.url_contains("checkout-complete"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".complete-header")))
        path = OUT / "08_order_confirmation.png"
        assert drv.get_screenshot_as_file(str(path))
        print("wrote", path, path.stat().st_size)
    finally:
        drv.quit()


if __name__ == "__main__":
    main()
