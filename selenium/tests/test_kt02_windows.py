"""КТ 02: открытие, переключение и закрытие окон браузера."""

from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def windows_main(driver, wait, fixture_url):
    """Open the local main-window fixture and remember its handle."""
    driver.get(fixture_url("kt02", "windows_main.html"))
    wait.until(EC.presence_of_element_located((By.ID, "main-heading")))
    original = driver.current_window_handle
    assert driver.title == "KT02 Main Window"
    return original


def _open_secondary_window(driver, wait, original_handle: str) -> str:
    before = set(driver.window_handles)
    link = wait.until(EC.element_to_be_clickable((By.ID, "open-new-window")))
    link.click()
    wait.until(EC.number_of_windows_to_be(len(before) + 1))
    new_handles = set(driver.window_handles) - before
    assert len(new_handles) == 1
    new_handle = new_handles.pop()
    assert new_handle != original_handle
    return new_handle


@pytest.mark.kt02
def test_open_new_browser_window(driver, wait, save_screenshot, windows_main):
    """Opening the link creates a second browser window/tab."""
    assert len(driver.window_handles) == 1
    save_screenshot("kt02", "01_main_window_before_open")

    new_handle = _open_secondary_window(driver, wait, windows_main)

    assert len(driver.window_handles) == 2
    assert new_handle in driver.window_handles
    save_screenshot("kt02", "02_after_open_still_on_main")


@pytest.mark.kt02
def test_switch_to_new_window_by_handle(driver, wait, save_screenshot, windows_main):
    """Switch to the secondary window using window handles."""
    new_handle = _open_secondary_window(driver, wait, windows_main)
    assert driver.current_window_handle == windows_main

    driver.switch_to.window(new_handle)

    wait.until(EC.title_is("KT02 New Window"))
    assert driver.current_window_handle == new_handle
    save_screenshot("kt02", "03_switched_to_new_window")


@pytest.mark.kt02
def test_verify_new_window_content(driver, wait, save_screenshot, windows_main):
    """Secondary window shows the expected heading and body text."""
    new_handle = _open_secondary_window(driver, wait, windows_main)
    driver.switch_to.window(new_handle)

    heading = wait.until(EC.visibility_of_element_located((By.ID, "new-heading")))
    body = wait.until(EC.visibility_of_element_located((By.ID, "new-body")))

    assert heading.text.strip() == "Содержимое нового окна"
    assert "вторичное окно" in body.text.lower()
    assert "windows_new.html" in driver.current_url
    save_screenshot("kt02", "04_new_window_content_verified")


@pytest.mark.kt02
def test_close_secondary_and_return_to_original(
    driver, wait, save_screenshot, windows_main
):
    """Close the secondary window and return to the original context."""
    new_handle = _open_secondary_window(driver, wait, windows_main)
    driver.switch_to.window(new_handle)
    wait.until(EC.visibility_of_element_located((By.ID, "new-heading")))
    save_screenshot("kt02", "05_before_close_secondary")

    driver.close()
    wait.until(EC.number_of_windows_to_be(1))
    assert new_handle not in driver.window_handles

    driver.switch_to.window(windows_main)

    main_heading = wait.until(EC.visibility_of_element_located((By.ID, "main-heading")))
    assert driver.current_window_handle == windows_main
    assert main_heading.text.strip() == "Главное окно KT02"
    assert driver.title == "KT02 Main Window"
    save_screenshot("kt02", "06_returned_to_main_window")
