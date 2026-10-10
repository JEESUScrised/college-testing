from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .base import SauceBasePage


class SauceInventoryPage(SauceBasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "inventory_item")
    SORT = (By.CLASS_NAME, "product_sort_container")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def wait_loaded(self) -> "SauceInventoryPage":
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        assert self.driver.find_element(*self.TITLE).text.strip() == "Products"
        return self

    def product_count(self) -> int:
        return len(self.driver.find_elements(*self.ITEMS))

    def open_first_product(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.ITEM_NAME)).click()

    def add_first_product(self) -> str:
        btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(.,'Add to cart')])[1]"))
        )
        name = btn.get_attribute("data-test") or "item"
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        return name

    def sort_by_value(self, value: str) -> None:
        el = self.wait.until(EC.element_to_be_clickable(self.SORT))
        Select(el).select_by_value(value)
        el = self.wait.until(EC.presence_of_element_located(self.SORT))
        assert Select(el).first_selected_option.get_attribute("value") == value
