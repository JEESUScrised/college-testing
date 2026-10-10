"""KT08 — public website screenshot tests with Allure reporting.

Selected site: https://www.saucedemo.com/
Reason: https://the-internet.herokuapp.com/ returns an empty/blocked DOM under
Chrome automation on this machine (bot protection / challenge script), while
Sauce Demo loads reliably and exposes login + inventory UI controls.
"""

from __future__ import annotations

from pathlib import Path

import allure
import pytest
from allure_commons.types import Severity
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from visual.allure_helpers import attach_png, attach_text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SHOTS = PROJECT_ROOT / "screenshots" / "kt08"
BASE_URL = "https://www.saucedemo.com"
VIEWPORT = (1400, 1000)
USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def public_driver(driver):
    driver.set_window_size(*VIEWPORT)
    driver.set_page_load_timeout(30)
    caps = getattr(driver, "capabilities", {}) or {}
    attach_text(
        f"browserName={caps.get('browserName')}\n"
        f"browserVersion={caps.get('browserVersion')}\n"
        f"viewport={VIEWPORT[0]}x{VIEWPORT[1]}\n"
        f"base_url={BASE_URL}\n"
        f"pageLoadStrategy=eager\n"
        f"note=the-internet.herokuapp.com blocked under Chrome automation; "
        f"saucedemo.com selected as accessible public demo\n",
        "browser-environment",
    )
    return driver


@pytest.fixture
def public_wait(public_driver):
    return WebDriverWait(public_driver, 15)


def _open(driver, wait: WebDriverWait, path: str = "/") -> None:
    url = f"{BASE_URL}{path}"
    try:
        driver.get(url)
    except TimeoutException:
        pass
    wait.until(
        lambda d: d.execute_script("return document.readyState")
        in ("interactive", "complete")
    )


def _shot(driver, name: str) -> Path:
    SHOTS.mkdir(parents=True, exist_ok=True)
    path = SHOTS / f"{name}.png"
    assert driver.save_screenshot(str(path)), path
    assert path.stat().st_size > 0
    attach_png(path, name)
    return path


def _login(driver, wait: WebDriverWait) -> None:
    _open(driver, wait, "/")
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).clear()
    driver.find_element(By.ID, "user-name").send_keys(USER)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))


@allure.epic("KT08 Screenshot Testing")
@allure.feature("Public website — saucedemo.com")
@allure.story("Login page / navigation branding")
@allure.title("TC-08-P01 Login page opens with branding and form")
@allure.description(
    "Open Sauce Demo public login page, verify logo/branding and login form "
    "controls, attach a screenshot to Allure."
)
@allure.severity(Severity.CRITICAL)
@pytest.mark.kt08
@pytest.mark.kt08_public
def test_public_login_page_and_branding(public_driver, public_wait):
    with allure.step(f"Open {BASE_URL}/"):
        _open(public_driver, public_wait, "/")
        public_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "login_logo")))
        assert "Swag Labs" in public_driver.title or public_driver.find_element(
            By.CLASS_NAME, "login_logo"
        ).is_displayed()

    with allure.step("Verify login form controls"):
        username = public_wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        password = public_driver.find_element(By.ID, "password")
        login_btn = public_driver.find_element(By.ID, "login-button")
        assert username.is_displayed() and password.is_displayed() and login_btn.is_displayed()
        # Accepted usernames hint is part of the public demo UI
        assert public_driver.find_element(By.ID, "login_credentials").is_displayed()

    with allure.step("Capture login page screenshot for Allure"):
        _shot(public_driver, "public_01_login_page")


@allure.epic("KT08 Screenshot Testing")
@allure.feature("Public website — saucedemo.com")
@allure.story("Authenticated inventory page")
@allure.title("TC-08-P02 Successful login shows inventory products")
@allure.description(
    "Log in with the documented public demo credentials and verify the inventory "
    "page with product cards before attaching a screenshot."
)
@allure.severity(Severity.CRITICAL)
@pytest.mark.kt08
@pytest.mark.kt08_public
def test_public_inventory_after_login(public_driver, public_wait):
    with allure.step("Login as standard_user"):
        _login(public_driver, public_wait)

    with allure.step("Verify inventory UI"):
        title = public_wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title"))
        )
        assert title.text.strip() == "Products"
        items = public_driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) >= 6
        attach_text(f"product_cards={len(items)}", "inventory-count")

    with allure.step("Capture inventory screenshot"):
        _shot(public_driver, "public_02_inventory")


@allure.epic("KT08 Screenshot Testing")
@allure.feature("Public website — saucedemo.com")
@allure.story("Interactive controls")
@allure.title("TC-08-P03 Product sort dropdown changes selection")
@allure.description(
    "On the inventory page, change the product sort dropdown and verify the "
    "selected option, then attach a screenshot."
)
@allure.severity(Severity.NORMAL)
@pytest.mark.kt08
@pytest.mark.kt08_public
def test_public_sort_dropdown(public_driver, public_wait):
    with allure.step("Login and open inventory"):
        _login(public_driver, public_wait)

    with allure.step("Select Name (Z to A) in sort dropdown"):
        select_el = public_wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container"))
        )
        Select(select_el).select_by_value("za")
        # Re-find after React re-render to avoid stale element.
        select_el = public_wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
        )
        selected = Select(select_el).first_selected_option
        assert selected.get_attribute("value") == "za"
        assert "Z to A" in selected.text
        attach_text(f"selected={selected.text} value=za", "dropdown-selection")

    with allure.step("Capture dropdown screenshot"):
        _shot(public_driver, "public_03_sort_dropdown")


@allure.epic("KT08 Screenshot Testing")
@allure.feature("Public website — saucedemo.com")
@allure.story("Interactive controls")
@allure.title("TC-08-P04 Add to cart updates cart badge")
@allure.description(
    "Click Add to cart on the first product and verify the cart badge changes, "
    "then attach a screenshot."
)
@allure.severity(Severity.NORMAL)
@pytest.mark.kt08
@pytest.mark.kt08_public
def test_public_add_to_cart(public_driver, public_wait):
    with allure.step("Login and open inventory"):
        _login(public_driver, public_wait)

    with allure.step("Add first visible product to cart"):
        badge_before = public_driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert badge_before == []
        add_btn = public_wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//button[contains(.,'Add to cart')])[1]")
            )
        )
        product = add_btn.get_attribute("data-test") or "unknown"
        public_driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", add_btn
        )
        public_driver.execute_script("arguments[0].click();", add_btn)
        badge = public_wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert badge.text.strip() == "1"
        attach_text(f"cart_badge=1 product={product}", "cart-state")

    with allure.step("Capture cart interaction screenshot"):
        _shot(public_driver, "public_04_add_to_cart")
