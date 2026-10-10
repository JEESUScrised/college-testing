"""KT02 remediation — public Sauce Demo functional testing techniques.

Preserves historical local windows/iframe suites. Demonstrates positive,
negative, boundary, multi-locator, cookie, and window-handle techniques.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.sauce import (
    SauceCartPage,
    SauceCheckoutPage,
    SauceInventoryPage,
    SauceLoginPage,
    SauceProductPage,
)
from pages.sauce.base import BASE_URL, DEFAULT_PASSWORD, DEFAULT_USER

SHOTS = Path(__file__).resolve().parents[2] / "screenshots" / "kt02" / "public"


@pytest.fixture
def sauce_driver(driver):
    driver.set_window_size(1400, 1000)
    driver.set_page_load_timeout(25)
    try:
        driver.get(BASE_URL + "/")
    except TimeoutException:
        pass
    return driver


@pytest.fixture
def sauce_wait(sauce_driver):
    return WebDriverWait(sauce_driver, 12)


def _shot(driver, name: str) -> Path:
    SHOTS.mkdir(parents=True, exist_ok=True)
    path = SHOTS / f"{name}.png"
    assert driver.save_screenshot(str(path))
    return path


# --- Positive ---


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_positive_login_inventory(sauce_driver, sauce_wait):
    page = SauceLoginPage(sauce_driver).open_login()
    page.login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    assert inv.product_count() >= 6
    _shot(sauce_driver, "pos_01_inventory")


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_positive_product_details_and_cart(sauce_driver, sauce_wait):
    SauceLoginPage(sauce_driver).open_login().login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    inv.open_first_product()
    product = SauceProductPage(sauce_driver).wait_loaded()
    name = product.product_name()
    assert name
    product.add_to_cart()
    product.go_to_cart()
    cart = SauceCartPage(sauce_driver).wait_loaded()
    assert cart.item_count() == 1
    _shot(sauce_driver, "pos_02_cart")


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_positive_remove_and_checkout(sauce_driver, sauce_wait):
    SauceLoginPage(sauce_driver).open_login().login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    inv.add_first_product()
    inv.go_to_cart()
    cart = SauceCartPage(sauce_driver).wait_loaded()
    cart.remove_first()
    assert cart.item_count() == 0
    inv = SauceInventoryPage(sauce_driver)
    # return via continue shopping if needed — re-add and checkout
    sauce_driver.get(BASE_URL + "/inventory.html")
    SauceInventoryPage(sauce_driver).wait_loaded().add_first_product()
    SauceInventoryPage(sauce_driver).go_to_cart()
    SauceCartPage(sauce_driver).wait_loaded().checkout()
    checkout = SauceCheckoutPage(sauce_driver).wait_info_loaded()
    checkout.fill_info("Ann", "Tester", "12345")
    checkout.continue_to_overview()
    checkout.finish()
    assert "Thank you" in checkout.complete_text()
    _shot(sauce_driver, "pos_03_checkout_complete")


# --- Negative ---


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_negative_empty_username(sauce_driver):
    page = SauceLoginPage(sauce_driver).open_login()
    page.login(username="", password=DEFAULT_PASSWORD)
    err = page.error_text()
    assert "Username is required" in err
    _shot(sauce_driver, "neg_01_empty_username")


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_negative_empty_password(sauce_driver):
    page = SauceLoginPage(sauce_driver).open_login()
    page.login(username=DEFAULT_USER, password="")
    err = page.error_text()
    assert "Password is required" in err
    _shot(sauce_driver, "neg_02_empty_password")


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_negative_bad_credentials(sauce_driver):
    page = SauceLoginPage(sauce_driver).open_login()
    page.login(username="locked_out_user", password="wrong")
    err = page.error_text().lower()
    assert "do not match" in err or "locked" in err or "epic sadface" in err
    _shot(sauce_driver, "neg_03_bad_credentials")


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_negative_checkout_missing_fields(sauce_driver):
    SauceLoginPage(sauce_driver).open_login().login()
    SauceInventoryPage(sauce_driver).wait_loaded().add_first_product()
    SauceInventoryPage(sauce_driver).go_to_cart()
    SauceCartPage(sauce_driver).wait_loaded().checkout()
    checkout = SauceCheckoutPage(sauce_driver).wait_info_loaded()
    checkout.continue_checkout()
    err = checkout.error_text()
    assert "First Name" in err or "required" in err.lower()
    _shot(sauce_driver, "neg_04_checkout_required")


# --- Boundary (checkout postal / name length adjacent) ---


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_boundary_checkout_zip_values(sauce_driver):
    """Boundary on postal-code: empty (reject) vs minimal non-empty '1' (accept step)."""
    SauceLoginPage(sauce_driver).open_login().login()
    SauceInventoryPage(sauce_driver).wait_loaded().add_first_product()
    SauceInventoryPage(sauce_driver).go_to_cart()
    SauceCartPage(sauce_driver).wait_loaded().checkout()
    checkout = SauceCheckoutPage(sauce_driver).wait_info_loaded()

    # empty zip with names filled → Postal Code required
    checkout.fill_info("A", "B", "")
    checkout.continue_checkout()
    err = checkout.error_text()
    assert "Postal Code" in err or "postal" in err.lower()
    _shot(sauce_driver, "bound_01_empty_zip")

    # minimal accepted non-empty zip
    checkout.fill_info("A", "B", "1")
    checkout.continue_to_overview()
    assert "checkout-step-two" in sauce_driver.current_url
    _shot(sauce_driver, "bound_02_min_zip")


# --- Locators diversity + cookies + window ---


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_locators_strategies(sauce_driver):
    SauceLoginPage(sauce_driver).open_login()
    # ID
    assert sauce_driver.find_element(By.ID, "user-name").is_displayed()
    # CSS
    assert sauce_driver.find_element(By.CSS_SELECTOR, "[data-test='username']").is_displayed()
    # Name
    assert sauce_driver.find_element(By.NAME, "password").is_displayed()
    # XPath
    assert sauce_driver.find_element(By.XPATH, "//input[@id='login-button']").is_displayed()
    _shot(sauce_driver, "tech_01_locators")


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_cookie_management(sauce_driver):
    SauceLoginPage(sauce_driver).open_login()
    # domain context established
    sauce_driver.delete_cookie("kt02_probe")
    sauce_driver.add_cookie({"name": "kt02_probe", "value": "alpha-42", "path": "/"})
    got = sauce_driver.get_cookie("kt02_probe")
    assert got and got["value"] == "alpha-42"
    sauce_driver.delete_cookie("kt02_probe")
    assert sauce_driver.get_cookie("kt02_probe") is None
    # After login Sauce sets session-username cookie
    SauceLoginPage(sauce_driver).login()
    SauceInventoryPage(sauce_driver).wait_loaded()
    session = sauce_driver.get_cookie("session-username")
    assert session and session["value"] == DEFAULT_USER
    _shot(sauce_driver, "tech_02_cookies")


@pytest.mark.kt02
@pytest.mark.kt02_public
def test_kt02_window_handles_public(sauce_driver, sauce_wait):
    SauceLoginPage(sauce_driver).open_login().login()
    SauceInventoryPage(sauce_driver).wait_loaded()
    main = sauce_driver.current_window_handle
    sauce_driver.execute_script("window.open(arguments[0], '_blank');", BASE_URL + "/")
    sauce_wait.until(EC.number_of_windows_to_be(2))
    handles = [h for h in sauce_driver.window_handles if h != main]
    sauce_driver.switch_to.window(handles[0])
    SauceLoginPage(sauce_driver).open_login()
    assert SauceLoginPage(sauce_driver).form_controls_visible()
    _shot(sauce_driver, "tech_03_secondary_tab")
    sauce_driver.close()
    sauce_driver.switch_to.window(main)
    assert "inventory" in sauce_driver.current_url
