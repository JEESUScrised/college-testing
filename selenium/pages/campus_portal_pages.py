"""Page Objects for the KT04 educational Campus Portal Demo."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = ("kt04", "index.html")

    HEADING = (By.ID, "login-heading")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "login-submit")
    ERROR = (By.ID, "login-error")
    GO_REGISTER = (By.ID, "go-register")

    def open_fixture(self, fixture_url) -> "LoginPage":
        self.open(fixture_url(*self.PATH))
        self.find_visible(self.HEADING)
        return self

    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def error_visible(self) -> bool:
        element = self.find(self.ERROR)
        return element.is_displayed()

    def open_register(self) -> None:
        self.click(self.GO_REGISTER)


class RegisterPage(BasePage):
    PATH = ("kt04", "register.html")

    HEADING = (By.ID, "register-heading")
    NAME = (By.ID, "reg-name")
    EMAIL = (By.ID, "reg-email")
    PASSWORD = (By.ID, "reg-password")
    SUBMIT = (By.ID, "register-submit")
    ERROR = (By.ID, "register-error")
    SUCCESS = (By.ID, "register-success")

    def open_fixture(self, fixture_url) -> "RegisterPage":
        self.open(fixture_url(*self.PATH))
        self.find_visible(self.HEADING)
        return self

    def register(self, name: str, email: str, password: str) -> None:
        self.type_text(self.NAME, name)
        self.type_text(self.EMAIL, email)
        self.type_text(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def success_visible(self) -> bool:
        return self.find(self.SUCCESS).is_displayed()

    def error_visible(self) -> bool:
        return self.find(self.ERROR).is_displayed()

    def success_text(self) -> str:
        return self.text_of(self.SUCCESS)

    def error_text(self) -> str:
        return self.text_of(self.ERROR)


class DashboardPage(BasePage):
    PATH = ("kt04", "dashboard.html")

    HEADING = (By.ID, "dash-heading")
    USER_LABEL = (By.ID, "user-label")
    QUANTITY = (By.ID, "quantity")
    SUBMIT = (By.ID, "order-submit")
    ERROR = (By.ID, "order-error")
    SUCCESS = (By.ID, "order-success")

    def wait_loaded(self) -> "DashboardPage":
        self.wait_until_title_is("Campus Portal Demo — Кабинет")
        self.find_visible(self.HEADING)
        return self

    def user_label(self) -> str:
        return self.text_of(self.USER_LABEL)

    def place_order(self, quantity: str) -> None:
        self.type_text(self.QUANTITY, quantity)
        self.click(self.SUBMIT)

    def success_visible(self) -> bool:
        self.wait.until(EC.any_of(
            EC.visibility_of_element_located(self.SUCCESS),
            EC.visibility_of_element_located(self.ERROR),
        ))
        return self.find(self.SUCCESS).is_displayed()

    def error_visible(self) -> bool:
        self.wait.until(EC.any_of(
            EC.visibility_of_element_located(self.SUCCESS),
            EC.visibility_of_element_located(self.ERROR),
        ))
        return self.find(self.ERROR).is_displayed()

    def success_text(self) -> str:
        return self.text_of(self.SUCCESS)
