"""Shared Selenium helpers for Page Object classes."""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class BasePage:
    """Common navigation, lookup, click, type and wait helpers."""

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def current_window_handle(self) -> str:
        return self.driver.current_window_handle

    @property
    def window_handles(self) -> list[str]:
        return list(self.driver.window_handles)

    def find(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple[str, str]) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator: tuple[str, str], text: str, *, clear: bool = True) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        if clear:
            element.clear()
        element.send_keys(text)

    def text_of(self, locator: tuple[str, str]) -> str:
        return self.find_visible(locator).text.strip()

    def wait_until_title_is(self, title: str) -> None:
        self.wait.until(EC.title_is(title))

    def wait_until_windows_count(self, count: int) -> None:
        self.wait.until(EC.number_of_windows_to_be(count))

    def switch_to_window(self, handle: str) -> None:
        self.driver.switch_to.window(handle)

    def close_current_window(self) -> None:
        self.driver.close()

    def switch_to_frame(self, locator: tuple[str, str]) -> None:
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()

    def count_elements(self, locator: tuple[str, str]) -> int:
        # Avoid the full implicit-wait delay when expecting zero matches.
        self.driver.implicitly_wait(0)
        try:
            return len(self.driver.find_elements(*locator))
        finally:
            self.driver.implicitly_wait(5)
