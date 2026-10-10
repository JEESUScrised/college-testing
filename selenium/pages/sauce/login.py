from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base import DEFAULT_PASSWORD, DEFAULT_USER, SauceBasePage


class SauceLoginPage(SauceBasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    LOGO = (By.CLASS_NAME, "login_logo")

    def open_login(self) -> "SauceLoginPage":
        self.open("/")
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        return self

    def login(self, username: str = DEFAULT_USER, password: str = DEFAULT_PASSWORD) -> None:
        user = self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        user.clear()
        user.send_keys(username)
        pwd = self.driver.find_element(*self.PASSWORD)
        pwd.clear()
        pwd.send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()

    def error_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ERROR)).text

    def form_controls_visible(self) -> bool:
        return all(
            self.driver.find_element(*loc).is_displayed()
            for loc in (self.USERNAME, self.PASSWORD, self.LOGIN_BTN, self.LOGO)
        )
