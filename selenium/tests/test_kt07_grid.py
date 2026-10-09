"""КТ 07: удалённые WebDriver-сессии через Selenium Grid 4."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.iframe_page import IframePage
from pages.windows_page import WindowsMainPage, WindowsSecondaryPage

ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts" / "kt07"


@pytest.mark.kt07
def test_remote_session_created(grid_driver, save_grid_screenshot):
    """Создаётся реальная RemoteWebDriver-сессия через Grid (не local Chrome)."""
    assert isinstance(grid_driver, RemoteWebDriver)
    assert not isinstance(grid_driver, webdriver.Chrome)
    assert grid_driver.session_id, "session_id must be non-empty"

    caps = grid_driver.capabilities
    browser = (caps.get("browserName") or "").lower()
    assert browser in {"chrome", "chromium"}, caps

    # Command executor points at Grid, not a local driver service
    client_config = getattr(grid_driver.command_executor, "client_config", None)
    remote_addr = getattr(client_config, "remote_server_addr", "") if client_config else ""
    assert "127.0.0.1:4444" in remote_addr or "localhost:4444" in remote_addr, remote_addr

    save_grid_screenshot("01_remote_session_blank")
    meta = {
        "session_id": grid_driver.session_id,
        "browserName": caps.get("browserName"),
        "browserVersion": caps.get("browserVersion"),
        "platformName": caps.get("platformName"),
        "se:cdp": caps.get("se:cdp"),
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "diag_session_caps.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


@pytest.mark.kt07
def test_navigate_and_title(grid_driver, grid_wait, fixture_http_url, save_grid_screenshot):
    """Навигация на локальную HTTP-фикстуру и проверка title."""
    url = fixture_http_url("kt07", "index.html")
    grid_driver.get(url)
    grid_wait.until(EC.title_is("KT07 Grid Landing"))
    heading = grid_wait.until(EC.visibility_of_element_located((By.ID, "heading")))
    assert heading.text.strip() == "Selenium Grid KT07"
    assert url in grid_driver.current_url
    save_grid_screenshot("02_navigate_title")


@pytest.mark.kt07
def test_dom_element_interaction(
    grid_driver, grid_wait, fixture_http_url, save_grid_screenshot
):
    """Взаимодействие с DOM: ввод текста и проверка статуса."""
    grid_driver.get(fixture_http_url("kt07", "index.html"))
    field = grid_wait.until(EC.element_to_be_clickable((By.ID, "name-input")))
    field.clear()
    field.send_keys("KT07 Remote")
    grid_wait.until(EC.element_to_be_clickable((By.ID, "submit-btn"))).click()
    status = grid_wait.until(EC.visibility_of_element_located((By.ID, "status")))
    grid_wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "KT07 Remote"))
    assert "принято — KT07 Remote" in status.text
    save_grid_screenshot("03_dom_interaction")


@pytest.mark.kt07
def test_window_open_and_switch(
    grid_driver, grid_wait, fixture_http_url, save_grid_screenshot
):
    """Открытие вторичного окна и переключение по window handles через Grid."""
    main = WindowsMainPage(grid_driver)
    main.open(fixture_http_url("kt02", "windows_main.html"))
    grid_wait.until(EC.title_is(WindowsMainPage.EXPECTED_TITLE))
    original = grid_driver.current_window_handle
    assert len(grid_driver.window_handles) == 1
    save_grid_screenshot("04_windows_main")

    new_handle = main.open_secondary_window()
    grid_driver.switch_to.window(new_handle)
    secondary = WindowsSecondaryPage(grid_driver)
    grid_wait.until(EC.title_is(WindowsSecondaryPage.EXPECTED_TITLE))
    assert secondary.heading_text() == WindowsSecondaryPage.EXPECTED_HEADING
    save_grid_screenshot("05_windows_secondary")

    secondary.close_and_return_to(original)
    assert grid_driver.current_window_handle == original
    assert main.heading_text() == WindowsMainPage.EXPECTED_HEADING
    save_grid_screenshot("06_windows_back_main")


@pytest.mark.kt07
def test_iframe_interaction_and_context_switch(
    grid_driver, grid_wait, fixture_http_url, save_grid_screenshot
):
    """Переключение в iframe, ввод данных и возврат в default_content."""
    page = IframePage(grid_driver)
    page.open(fixture_http_url("kt02", "iframe_host.html"))
    grid_wait.until(EC.title_is(IframePage.EXPECTED_TITLE))
    assert page.host_heading_text() == IframePage.EXPECTED_HOST_HEADING
    save_grid_screenshot("07_iframe_host")

    page.enter_iframe()
    assert page.frame_heading_text() == IframePage.EXPECTED_FRAME_HEADING
    result = page.submit_frame_value("KT07 iframe via Grid")
    assert "KT07 iframe via Grid" in result
    save_grid_screenshot("08_iframe_inside")

    page.leave_iframe()
    assert page.host_footer_text() == "Подвал основного документа"
    assert page.frame_input_visible_in_current_context() is False
    # Make the host-context screenshot visually distinct from the in-frame shot
    grid_driver.execute_script(
        "document.getElementById('host-status').textContent="
        "'Контекст: снова основной документ (KT07)';"
    )
    grid_wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "host-status"), "снова основной документ"
        )
    )
    save_grid_screenshot("09_iframe_default_content")
