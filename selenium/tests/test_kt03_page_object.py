"""КТ 03: сценарии окон и iframe через Page Object."""

from __future__ import annotations

import pytest

from pages.iframe_page import IframePage
from pages.windows_page import WindowsMainPage, WindowsSecondaryPage


@pytest.mark.kt03
def test_po_open_secondary_window(driver, fixture_url, save_screenshot):
    """Page Object opens a second window from the main fixture page."""
    main = WindowsMainPage(driver).open_fixture(fixture_url)
    save_screenshot("kt03", "01_po_main_before_open")

    assert main.title == WindowsMainPage.EXPECTED_TITLE
    assert len(main.window_handles) == 1

    new_handle = main.open_secondary_window()

    assert len(main.window_handles) == 2
    assert new_handle in main.window_handles
    assert main.current_window_handle != new_handle
    assert main.heading_text() == WindowsMainPage.EXPECTED_HEADING
    save_screenshot("kt03", "02_po_after_open_on_main")


@pytest.mark.kt03
def test_po_switch_and_verify_secondary_content(driver, fixture_url, save_screenshot):
    """Page Object switches by handle and exposes secondary-window content."""
    main = WindowsMainPage(driver).open_fixture(fixture_url)
    original = main.current_window_handle
    new_handle = main.open_secondary_window()

    secondary = WindowsSecondaryPage(driver).switch_to(new_handle)
    save_screenshot("kt03", "03_po_switched_to_secondary")

    assert secondary.current_window_handle == new_handle
    assert secondary.title == WindowsSecondaryPage.EXPECTED_TITLE
    assert secondary.heading_text() == WindowsSecondaryPage.EXPECTED_HEADING
    assert "вторичное окно" in secondary.body_text().lower()
    assert "windows_new.html" in secondary.current_url
    assert original in secondary.window_handles
    save_screenshot("kt03", "04_po_secondary_content_verified")


@pytest.mark.kt03
def test_po_close_secondary_and_return(driver, fixture_url, save_screenshot):
    """Page Object closes the secondary window and returns to the original one."""
    main = WindowsMainPage(driver).open_fixture(fixture_url)
    original = main.current_window_handle
    new_handle = main.open_secondary_window()

    secondary = WindowsSecondaryPage(driver).switch_to(new_handle)
    save_screenshot("kt03", "05_po_before_close_secondary")
    secondary.close_and_return_to(original)

    assert new_handle not in main.window_handles
    assert len(main.window_handles) == 1
    assert main.current_window_handle == original
    assert main.title == WindowsMainPage.EXPECTED_TITLE
    assert main.heading_text() == WindowsMainPage.EXPECTED_HEADING
    save_screenshot("kt03", "06_po_returned_to_main")


@pytest.mark.kt03
def test_po_iframe_interact_and_return_to_default(
    driver, fixture_url, save_screenshot
):
    """Page Object enters iframe, interacts, then returns via default_content()."""
    page = IframePage(driver).open_fixture(fixture_url)
    save_screenshot("kt03", "07_po_iframe_host")

    assert page.title == IframePage.EXPECTED_TITLE
    assert page.host_heading_text() == IframePage.EXPECTED_HOST_HEADING
    assert page.host_status_text() == "Контекст: основной документ"

    page.enter_iframe()
    assert page.frame_heading_text() == IframePage.EXPECTED_FRAME_HEADING
    result = page.submit_frame_value("КТ03 Page Object OK")
    save_screenshot("kt03", "08_po_iframe_interaction")

    assert result == "Результат: КТ03 Page Object OK"

    page.leave_iframe()
    save_screenshot("kt03", "09_po_back_to_default_content")

    assert page.host_heading_text() == IframePage.EXPECTED_HOST_HEADING
    assert page.host_footer_text() == "Подвал основного документа"
    assert page.frame_input_visible_in_current_context() is False
