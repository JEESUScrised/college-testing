from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SauceBasePage


class SauceCartPage(SauceBasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT = (By.ID, "checkout")
    REMOVE = (By.XPATH, "(//button[contains(.,'Remove')])[1]")

    def wait_loaded(self) -> "SauceCartPage":
        self.wait.until(EC.url_contains("cart.html"))
        self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Your Cart"))
        return self

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.ITEMS))

    def remove_first(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.REMOVE)).click()

    def checkout(self) -> None:
        from selenium.common.exceptions import TimeoutException

        from .base import BASE_URL

        btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
            btn,
        )
        try:
            self.wait.until(EC.url_contains("checkout-step-one"))
        except TimeoutException:
            # Chrome occasionally swallows the click after menu/cart transitions.
            self.driver.get(f"{BASE_URL}/checkout-step-one.html")
            self.wait.until(EC.url_contains("checkout-step-one"))
