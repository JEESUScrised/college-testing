"""КТ 06: Appium UI-тесты официального ApiDemos (Android)."""

from __future__ import annotations

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from pages.api_demos_pages import AlertDialogsPage, ApiDemosHomePage, ViewsTextFieldsPage


def _open_path(driver, wait, *labels: str) -> None:
    """Open nested ApiDemos menu items by accessibility id (scroll if off-screen)."""
    page = ApiDemosHomePage(driver)
    for label in labels:
        page.click_menu_item(label)


@pytest.mark.kt06
def test_app_starts_and_shows_home(driver, wait, save_screenshot):
    """Приложение ApiDemos запускается и показывает список разделов."""
    home = ApiDemosHomePage(driver).wait_loaded()
    save_screenshot("kt06", "01_app_home")
    categories = home.visible_categories()
    assert "App" in categories or home.has_category("App")
    assert "Views" in categories or home.has_category("Views")


@pytest.mark.kt06
def test_navigate_to_app_menu(driver, wait, save_screenshot):
    """Навигация: Home → App."""
    ApiDemosHomePage(driver).wait_loaded()
    _open_path(driver, wait, "App")
    save_screenshot("kt06", "02_app_menu")
    wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Alert Dialogs")))
    assert driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Alert Dialogs").is_displayed()


@pytest.mark.kt06
def test_open_alert_dialogs_screen(driver, wait, save_screenshot):
    """Навигация: App → Alert Dialogs."""
    ApiDemosHomePage(driver).wait_loaded()
    _open_path(driver, wait, "App", "Alert Dialogs")
    page = AlertDialogsPage(driver).wait_loaded()
    save_screenshot("kt06", "03_alert_dialogs")
    assert page.find_visible(page.LIST_DIALOG).is_displayed()


@pytest.mark.kt06
def test_list_dialog_interaction(driver, wait, save_screenshot):
    """Нажатие List dialog открывает диалог; выбор пункта закрывает его."""
    ApiDemosHomePage(driver).wait_loaded()
    _open_path(driver, wait, "App", "Alert Dialogs")
    page = AlertDialogsPage(driver).wait_loaded()
    page.open_list_dialog()
    save_screenshot("kt06", "04_list_dialog")
    title = page.alert_title()
    assert title, "Alert title should be visible"
    # List dialog dismisses via list item (no OK button)
    item = (AppiumBy.ID, "android:id/text1")
    wait.until(EC.element_to_be_clickable(item)).click()
    wait.until(EC.invisibility_of_element_located(page.ALERT_TITLE))


@pytest.mark.kt06
def test_text_entry_dialog_input(driver, wait, save_screenshot):
    """Text Entry dialog: ввод username и проверка значения поля."""
    ApiDemosHomePage(driver).wait_loaded()
    _open_path(driver, wait, "App", "Alert Dialogs")
    page = AlertDialogsPage(driver).wait_loaded()
    page.open_text_entry_dialog()
    page.fill_text_entry("kt06_user", "secret")
    save_screenshot("kt06", "05_text_entry_dialog")
    assert "kt06_user" in (page.username_value() or "")
    page.confirm_dialog()


@pytest.mark.kt06
def test_back_returns_to_previous_screen(driver, wait, save_screenshot):
    """Системная кнопка Back возвращает с Alert Dialogs на App."""
    home = ApiDemosHomePage(driver).wait_loaded()
    _open_path(driver, wait, "App", "Alert Dialogs")
    AlertDialogsPage(driver).wait_loaded()
    home.press_back()
    wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Alert Dialogs")))
    save_screenshot("kt06", "06_back_to_app_menu")
    assert driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Alert Dialogs").is_displayed()
    home.press_back()
    ApiDemosHomePage(driver).wait_loaded()
    save_screenshot("kt06", "07_back_to_home")


@pytest.mark.kt06
def test_views_textfields_input(driver, wait, save_screenshot):
    """Views → TextFields: ввод текста и проверка содержимого EditText."""
    ApiDemosHomePage(driver).wait_loaded()
    _open_path(driver, wait, "Views", "TextFields")
    page = ViewsTextFieldsPage(driver).wait_loaded()
    page.enter_text("KT06 Appium OK")
    save_screenshot("kt06", "08_textfields")
    assert "KT06 Appium OK" in page.value()
