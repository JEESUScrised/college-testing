"""KT03 remediation — public Sauce Demo via shared Page Objects.

Historical local windows/iframe PO suite is preserved in test_kt03_page_object.py.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from selenium.common.exceptions import TimeoutException

from pages.sauce import (
    SauceCartPage,
    SauceCheckoutPage,
    SauceInventoryPage,
    SauceLoginPage,
    SauceProductPage,
)
from pages.sauce.base import BASE_URL

SHOTS = Path(__file__).resolve().parents[2] / "screenshots" / "kt03" / "public"


@pytest.fixture
def sauce_driver(driver):
    driver.set_window_size(1400, 1000)
    driver.set_page_load_timeout(25)
    try:
        driver.get(BASE_URL + "/")
    except TimeoutException:
        pass
    return driver


def _shot(driver, name: str) -> None:
    SHOTS.mkdir(parents=True, exist_ok=True)
    assert driver.save_screenshot(str(SHOTS / f"{name}.png"))


@pytest.mark.kt03
@pytest.mark.kt03_public
def test_po_login_page_opens_and_authenticates(sauce_driver):
    login = SauceLoginPage(sauce_driver).open_login()
    assert login.form_controls_visible()
    _shot(sauce_driver, "po_01_login_form")
    login.login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    assert inv.product_count() >= 6
    _shot(sauce_driver, "po_02_inventory_via_po")


@pytest.mark.kt03
@pytest.mark.kt03_public
def test_po_inventory_sort_and_open_product(sauce_driver):
    SauceLoginPage(sauce_driver).open_login().login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    inv.sort_by_value("lohi")
    assert inv.product_count() >= 6
    inv.open_first_product()
    product = SauceProductPage(sauce_driver).wait_loaded()
    assert product.product_name()
    _shot(sauce_driver, "po_03_product_details")


@pytest.mark.kt03
@pytest.mark.kt03_public
def test_po_product_add_and_cart(sauce_driver):
    SauceLoginPage(sauce_driver).open_login().login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    inv.open_first_product()
    product = SauceProductPage(sauce_driver).wait_loaded()
    product.add_to_cart()
    assert product.cart_badge_text() == "1"
    product.go_to_cart()
    cart = SauceCartPage(sauce_driver).wait_loaded()
    assert cart.item_count() == 1
    _shot(sauce_driver, "po_04_cart")


@pytest.mark.kt03
@pytest.mark.kt03_public
def test_po_checkout_flow(sauce_driver):
    SauceLoginPage(sauce_driver).open_login().login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    inv.add_first_product()
    inv.go_to_cart()
    SauceCartPage(sauce_driver).wait_loaded().checkout()
    checkout = SauceCheckoutPage(sauce_driver).wait_info_loaded()
    assert checkout.fields_visible()
    checkout.fill_info("Pat", "Object", "90210")
    checkout.continue_to_overview()
    checkout.finish()
    assert "Thank you" in checkout.complete_text()
    _shot(sauce_driver, "po_05_checkout_complete")


@pytest.mark.kt03
@pytest.mark.kt03_public
def test_po_menu_logout(sauce_driver):
    SauceLoginPage(sauce_driver).open_login().login()
    inv = SauceInventoryPage(sauce_driver).wait_loaded()
    inv.logout()
    login = SauceLoginPage(sauce_driver)
    assert login.form_controls_visible()
    _shot(sauce_driver, "po_06_logout")
