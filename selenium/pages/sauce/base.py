"""Base page for Sauce Demo."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com"
DEFAULT_USER = "standard_user"
DEFAULT_PASSWORD = "secret_sauce"


class SauceBasePage:
    URL = BASE_URL

    def __init__(self, driver: WebDriver, timeout: float = 15) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path: str = "/") -> None:
        self.driver.get(f"{BASE_URL}{path}")

    def viewport(self) -> dict:
        return self.driver.execute_script(
            "return {"
            "innerWidth: window.innerWidth,"
            "innerHeight: window.innerHeight,"
            "clientWidth: document.documentElement.clientWidth,"
            "scrollWidth: document.documentElement.scrollWidth,"
            "scrollHeight: document.documentElement.scrollHeight"
            "};"
        )

    def has_horizontal_overflow(self) -> bool:
        m = self.viewport()
        return int(m["scrollWidth"]) > int(m["clientWidth"]) + 1

    def open_menu(self) -> None:
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
        btn.click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "inventory_sidebar_link")))

    def close_menu(self) -> None:
        close = self.wait.until(EC.element_to_be_clickable((By.ID, "react-burger-cross-btn")))
        close.click()

    def cart_badge_text(self) -> str | None:
        badges = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        return badges[0].text.strip() if badges else None

    def go_to_cart(self) -> None:
        link = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        self.driver.execute_script("arguments[0].click();", link)
        self.wait.until(EC.url_contains("cart.html"))
