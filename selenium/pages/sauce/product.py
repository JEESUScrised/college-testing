from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SauceBasePage


class SauceProductPage(SauceBasePage):
    NAME = (By.CLASS_NAME, "inventory_details_name")
    ADD = (By.CSS_SELECTOR, "button.btn_inventory")
    BACK = (By.ID, "back-to-products")

    def wait_loaded(self) -> "SauceProductPage":
        self.wait.until(EC.visibility_of_element_located(self.NAME))
        return self

    def product_name(self) -> str:
        return self.driver.find_element(*self.NAME).text.strip()

    def add_to_cart(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.ADD)).click()
