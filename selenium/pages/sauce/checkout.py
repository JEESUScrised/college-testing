from __future__ import annotations

from selenium.common.exceptions import TimeoutException
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
            el = self.wait.until(EC.visibility_of_element_located(loc))
            # Native value setter keeps React controlled inputs in sync on Sauce Demo.
            self.driver.execute_script(
                "const el = arguments[0], v = arguments[1];"
                "const proto = window.HTMLInputElement.prototype;"
                "const desc = Object.getOwnPropertyDescriptor(proto, 'value');"
                "desc.set.call(el, v);"
                "el.dispatchEvent(new Event('input', {bubbles:true}));"
                "el.dispatchEvent(new Event('change', {bubbles:true}));",
                el,
                val,
            )
            if (el.get_attribute("value") or "") != val:
                el.clear()
                el.send_keys(val)

    def continue_checkout(self) -> None:
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE))
        # JS click avoids Chrome HTML5 "required" blocking the Sauce error banner.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
            btn,
        )

    def wait_overview_or_error(self) -> None:
        """After continue: either overview step or validation error must appear."""

        def _settled(driver) -> bool:
            if "checkout-step-two" in driver.current_url:
                return True
            errs = driver.find_elements(*self.ERROR)
            return any(e.is_displayed() and e.text.strip() for e in errs)

        try:
            self.wait.until(_settled)
        except TimeoutException:
            btn = self.driver.find_element(*self.CONTINUE)
            self.driver.execute_script("arguments[0].click();", btn)
            self.wait.until(_settled)

    def continue_to_overview(self) -> None:
        """Fill was already done; continue and require overview navigation."""
        self.continue_checkout()
        try:
            self.wait.until(EC.url_contains("checkout-step-two"))
        except TimeoutException:
            # Retry once after re-asserting field values via native setter path.
            for loc in (self.FIRST, self.LAST, self.ZIP):
                el = self.driver.find_element(*loc)
                val = el.get_attribute("value") or ""
                self.driver.execute_script(
                    "const el = arguments[0], v = arguments[1];"
                    "const proto = window.HTMLInputElement.prototype;"
                    "const desc = Object.getOwnPropertyDescriptor(proto, 'value');"
                    "desc.set.call(el, v);"
                    "el.dispatchEvent(new Event('input', {bubbles:true}));"
                    "el.dispatchEvent(new Event('change', {bubbles:true}));",
                    el,
                    val,
                )
            self.continue_checkout()
            self.wait.until(EC.url_contains("checkout-step-two"))

    def error_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ERROR)).text

    def fields_visible(self) -> bool:
        return all(
            self.driver.find_element(*loc).is_displayed()
            for loc in (self.FIRST, self.LAST, self.ZIP, self.CONTINUE)
        )

    def finish(self) -> None:
        btn = self.wait.until(EC.element_to_be_clickable(self.FINISH))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
            btn,
        )
        self.wait.until(EC.url_contains("checkout-complete"))

    def complete_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE)).text
