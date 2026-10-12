"""Recapture SauceDemo public screenshots for KT02 / KT03 / KT08 with visual settle."""

from __future__ import annotations

import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "selenium"))
from screenshot_ready import chrome_options_for_screenshots, wait_visually_ready  # noqa: E402

BASE = "https://www.saucedemo.com"
KT02 = ROOT / "screenshots" / "kt02" / "public"
KT03 = ROOT / "screenshots" / "kt03" / "public"
KT08 = ROOT / "screenshots" / "kt08"


def _driver():
    opts = ChromeOptions()
    opts.add_argument("--window-size=1400,1000")
    opts.page_load_strategy = "eager"
    chrome_options_for_screenshots(opts)
    drv = webdriver.Chrome(options=opts)
    drv.set_page_load_timeout(30)
    drv.implicitly_wait(0)
    return drv


def _shot(drv, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wait_visually_ready(drv)
    assert drv.save_screenshot(str(path)), path
    assert path.stat().st_size > 12_000, path
    print(f"  OK {path.relative_to(ROOT)} ({path.stat().st_size})")


def _login(drv, wait: WebDriverWait) -> None:
    drv.get(BASE + "/")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name"))).send_keys(
        "standard_user"
    )
    drv.find_element(By.CSS_SELECTOR, "#password").send_keys("secret_sauce")
    drv.find_element(By.CSS_SELECTOR, "#login-button").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item")))


def main() -> None:
    drv = _driver()
    wait = WebDriverWait(drv, 25)
    try:
        # --- Login form (shared) ---
        drv.get(BASE + "/")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#login-button")))
        _shot(drv, KT03 / "po_01_login_form.png")
        _shot(drv, KT08 / "public_01_login_page.png")

        # Negative login shots for KT02
        drv.find_element(By.CSS_SELECTOR, "#login-button").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        _shot(drv, KT02 / "neg_01_empty_username.png")

        drv.get(BASE + "/")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name"))).send_keys(
            "standard_user"
        )
        drv.find_element(By.CSS_SELECTOR, "#login-button").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        _shot(drv, KT02 / "neg_02_empty_password.png")

        drv.get(BASE + "/")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name"))).send_keys(
            "bad_user"
        )
        drv.find_element(By.CSS_SELECTOR, "#password").send_keys("bad_pass")
        drv.find_element(By.CSS_SELECTOR, "#login-button").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        _shot(drv, KT02 / "neg_03_bad_credentials.png")

        # Positive inventory / locators / cookies
        _login(drv, wait)
        _shot(drv, KT02 / "pos_01_inventory.png")
        _shot(drv, KT03 / "po_02_inventory_via_po.png")
        _shot(drv, KT08 / "public_02_inventory.png")
        _shot(drv, KT02 / "tech_01_locators.png")

        # Cookies evidence: stay on inventory with session cookie present
        cookies = drv.get_cookies()
        assert any(c.get("name") == "session-username" for c in cookies)
        _shot(drv, KT02 / "tech_02_cookies.png")

        # Sort dropdown KT08
        Select(drv.find_element(By.CSS_SELECTOR, ".product_sort_container")).select_by_value("za")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item")))
        _shot(drv, KT08 / "public_03_sort_dropdown.png")

        # Product details KT03 — re-find after React re-render from sort
        drv.get(BASE + "/inventory.html")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item_name")))
        name_el = drv.find_element(By.CSS_SELECTOR, ".inventory_item_name")
        drv.execute_script("arguments[0].click();", name_el)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_details_name")))
        _shot(drv, KT03 / "po_03_product_details.png")

        # Add to cart
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory")))
        drv.execute_script("arguments[0].click();", btn)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge")))
        _shot(drv, KT08 / "public_04_add_to_cart.png")

        # Cart
        drv.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()
        wait.until(EC.url_contains("cart.html"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart_item")))
        _shot(drv, KT02 / "pos_02_cart.png")
        _shot(drv, KT03 / "po_04_cart.png")

        # Secondary tab tech
        drv.execute_script("window.open(arguments[0], '_blank');", BASE + "/inventory.html")
        wait.until(lambda d: len(d.window_handles) >= 2)
        drv.switch_to.window(drv.window_handles[-1])
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item")))
        _shot(drv, KT02 / "tech_03_secondary_tab.png")
        drv.close()
        drv.switch_to.window(drv.window_handles[0])

        # Checkout validation empty
        drv.get(BASE + "/cart.html")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#checkout"))).click()
        wait.until(EC.url_contains("checkout-step-one"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#continue"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        _shot(drv, KT02 / "neg_04_checkout_required.png")
        _shot(drv, KT02 / "bound_01_empty_zip.png")

        # Min zip boundary then complete
        drv.find_element(By.CSS_SELECTOR, "#first-name").send_keys("QA")
        drv.find_element(By.CSS_SELECTOR, "#last-name").send_keys("Tester")
        drv.find_element(By.CSS_SELECTOR, "#postal-code").send_keys("1")
        _shot(drv, KT02 / "bound_02_min_zip.png")
        drv.find_element(By.CSS_SELECTOR, "#continue").click()
        wait.until(EC.url_contains("checkout-step-two"))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#finish"))).click()
        wait.until(EC.url_contains("checkout-complete"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".complete-header")))
        _shot(drv, KT02 / "pos_03_checkout_complete.png")
        _shot(drv, KT03 / "po_05_checkout_complete.png")

        # Logout
        drv.get(BASE + "/inventory.html")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-burger-menu-btn"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#logout_sidebar_link"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#login-button")))
        _shot(drv, KT03 / "po_06_logout.png")
    finally:
        drv.quit()
    print("DONE SauceDemo public recapture")


if __name__ == "__main__":
    main()
