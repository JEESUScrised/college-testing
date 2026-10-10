from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import SauceBasePage


class SauceCheckoutPage(SauceBasePage):
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    ZIP = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    COMPLETE = (By.CLASS_NAME, "complete-header")

    def wait_info_loaded(self) -> "SauceCheckoutPage":
        self.wait.until(EC.url_contains("checkout-step-one"))
        self.wait.until(EC.visibility_of_element_located(self.FIRST))
        return self

    def fill_info(self, first: str, last: str, zip_code: str) -> None:
        for loc, val in ((self.FIRST, first), (self.LAST, last), (self.ZIP, zip_code)):
            el = self.driver.find_element(*loc)
            el.clear()
            el.send_keys(val)

    def continue_checkout(self) -> None:
        btn = self.driver.find_element(*self.CONTINUE)
        # JS click avoids Chrome HTML5 "required" blocking the Sauce error banner.
        self.driver.execute_script("arguments[0].click();", btn)

    def error_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ERROR)).text

    def fields_visible(self) -> bool:
        return all(
            self.driver.find_element(*loc).is_displayed()
            for loc in (self.FIRST, self.LAST, self.ZIP, self.CONTINUE)
        )

    def finish(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.FINISH)).click()

    def complete_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE)).text
