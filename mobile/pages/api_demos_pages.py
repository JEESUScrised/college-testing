"""Page Objects for official Appium ApiDemos sample app."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BaseMobilePage


class ApiDemosHomePage(BaseMobilePage):
    """Launcher list of ApiDemos demo categories."""

    LIST = (AppiumBy.ID, "android:id/list")

    def wait_loaded(self) -> "ApiDemosHomePage":
        self.find(self.LIST)
        self.find_visible(self.by_accessibility_id("App"))
        return self

    def open_category(self, name: str) -> None:
        self.click(self.by_accessibility_id(name))

    def has_category(self, name: str) -> bool:
        self.driver.implicitly_wait(0)
        try:
            return len(self.driver.find_elements(*self.by_accessibility_id(name))) > 0
        finally:
            self.driver.implicitly_wait(0)

    def visible_categories(self) -> list[str]:
        items = self.driver.find_elements(
            AppiumBy.XPATH, "//android.widget.TextView[@resource-id='android:id/text1']"
        )
        return [(item.text or "").strip() for item in items if (item.text or "").strip()]


class AlertDialogsPage(BaseMobilePage):
    """App → Alert Dialogs screen."""

    LIST_DIALOG = (AppiumBy.ACCESSIBILITY_ID, "List dialog")
    TEXT_ENTRY_DIALOG = (AppiumBy.ACCESSIBILITY_ID, "Text Entry dialog")
    OK_BUTTON = (AppiumBy.ID, "android:id/button1")
    USERNAME = (AppiumBy.ID, "io.appium.android.apis:id/username_edit")
    PASSWORD = (AppiumBy.ID, "io.appium.android.apis:id/password_edit")
    ALERT_TITLE = (AppiumBy.ID, "android:id/alertTitle")

    def wait_loaded(self) -> "AlertDialogsPage":
        self.find_visible(self.LIST_DIALOG)
        return self

    def open_list_dialog(self) -> None:
        self.click(self.LIST_DIALOG)
        self.wait.until(EC.visibility_of_element_located(self.ALERT_TITLE))

    def open_text_entry_dialog(self) -> None:
        self.click(self.TEXT_ENTRY_DIALOG)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))

    def alert_title(self) -> str:
        return self.text_of(self.ALERT_TITLE)

    def fill_text_entry(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)

    def username_value(self) -> str:
        return self.find(self.USERNAME).text or self.find(self.USERNAME).get_attribute("text") or ""

    def confirm_dialog(self) -> None:
        self.click(self.OK_BUTTON)


class ViewsTextFieldsPage(BaseMobilePage):
    """Views → TextFields screen."""

    EDIT = (AppiumBy.ID, "io.appium.android.apis:id/edit")

    def wait_loaded(self) -> "ViewsTextFieldsPage":
        self.find_visible(self.EDIT)
        return self

    def enter_text(self, value: str) -> None:
        self.type_text(self.EDIT, value)

    def value(self) -> str:
        element = self.find(self.EDIT)
        return (element.text or element.get_attribute("text") or "").strip()
