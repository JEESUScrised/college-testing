"""Base helpers for Appium Android Page Objects."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15


class BaseMobilePage:
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple[str, str]) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def text_of(self, locator: tuple[str, str]) -> str:
        return (self.find_visible(locator).text or "").strip()

    def type_text(self, locator: tuple[str, str], value: str, *, clear: bool = True) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        if clear:
            element.clear()
        element.send_keys(value)

    def press_back(self) -> None:
        self.driver.back()

    def scroll_into_view_by_description(self, description: str) -> WebElement:
        """Scroll a scrollable list until accessibility/content-desc is visible."""
        # Escape double quotes for UiSelector string literal
        safe = description.replace("\\", "\\\\").replace('"', '\\"')
        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().description("{safe}"))',
        )
        return self.find(locator)

    def click_menu_item(self, name: str) -> None:
        """Open ApiDemos list item by accessibility id, scrolling if needed."""
        locator = self.by_accessibility_id(name)
        self.driver.implicitly_wait(0)
        try:
            visible = self.driver.find_elements(*locator)
            if not visible or not visible[0].is_displayed():
                self.scroll_into_view_by_description(name)
        finally:
            self.driver.implicitly_wait(0)
        self.click(locator)

    def by_accessibility_id(self, value: str) -> tuple[str, str]:
        return (AppiumBy.ACCESSIBILITY_ID, value)

    def by_id(self, value: str) -> tuple[str, str]:
        return (AppiumBy.ID, value)

    def by_xpath(self, value: str) -> tuple[str, str]:
        return (AppiumBy.XPATH, value)
