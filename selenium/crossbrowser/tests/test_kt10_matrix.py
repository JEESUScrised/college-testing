"""KT10 cross-browser matrix: 5 scenarios × chrome/firefox."""

from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

BROWSERS = ["chrome", "firefox"]


def _caps(driver) -> dict:
    # EventFiringWebDriver wraps wrapped driver
    raw = getattr(driver, "wrapped_driver", driver)
    return dict(raw.capabilities)


@pytest.mark.kt10
@pytest.mark.parametrize("kt10_browser", BROWSERS, indirect=True)
def test_open_page_title_and_url(kt10_driver, kt10_wait, kt10_url, kt10_shot, kt10_browser, kt10_listener):
    """Открытие страницы: title, URL и реальные capabilities браузера."""
    url = kt10_url("kt10", "home.html")
    kt10_driver.get(url)
    kt10_wait.until(EC.title_is("KT10 Cross-Browser Home"))
    assert "kt10/home.html" in kt10_driver.current_url
    heading = kt10_wait.until(EC.visibility_of_element_located((By.ID, "heading")))
    assert "KT10" in heading.text
    caps = _caps(kt10_driver)
    assert caps.get("browserName", "").lower() == kt10_browser
    assert caps.get("browserVersion"), caps
    kt10_shot("01_home_title")
    assert any(e["event"] == "after_navigate_to" for e in kt10_listener.events)


@pytest.mark.kt10
@pytest.mark.parametrize("kt10_browser", BROWSERS, indirect=True)
def test_dom_click_interaction(kt10_driver, kt10_wait, kt10_url, kt10_shot, kt10_listener):
    """Клик по DOM-элементу изменяет счётчик."""
    kt10_driver.get(kt10_url("kt10", "home.html"))
    btn = kt10_wait.until(EC.element_to_be_clickable((By.ID, "action-btn")))
    btn.click()
    counter = kt10_wait.until(EC.visibility_of_element_located((By.ID, "click-count")))
    assert counter.text.strip() == "Кликов: 1"
    kt10_shot("02_dom_click")
    assert any(e["event"] == "before_click" for e in kt10_listener.events)
    assert any(e["event"] == "after_click" for e in kt10_listener.events)


@pytest.mark.kt10
@pytest.mark.parametrize("kt10_browser", BROWSERS, indirect=True)
def test_form_input_and_validation(kt10_driver, kt10_wait, kt10_url, kt10_shot):
    """Ввод формы: ошибка валидации, затем успешная отправка."""
    kt10_driver.get(kt10_url("kt10", "home.html"))
    kt10_wait.until(EC.element_to_be_clickable((By.ID, "submit-btn"))).click()
    status = kt10_wait.until(EC.visibility_of_element_located((By.ID, "status")))
    assert "ошибка валидации" in status.text
    kt10_shot("03_form_invalid")

    email = kt10_driver.find_element(By.ID, "email")
    name = kt10_driver.find_element(By.ID, "name")
    email.clear()
    email.send_keys("kt10@example.com")
    name.clear()
    name.send_keys("KT10 User")
    kt10_driver.find_element(By.ID, "submit-btn").click()
    kt10_wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "принято"))
    assert "KT10 User" in status.text
    assert "kt10@example.com" in status.text
    kt10_shot("04_form_valid")


@pytest.mark.kt10
@pytest.mark.parametrize("kt10_browser", BROWSERS, indirect=True)
def test_window_switch(kt10_driver, kt10_wait, kt10_url, kt10_shot):
    """Открытие вкладки/окна и переключение по handles."""
    kt10_driver.get(kt10_url("kt02", "windows_main.html"))
    original = kt10_driver.current_window_handle
    kt10_wait.until(EC.title_is("KT02 Main Window"))
    before = set(kt10_driver.window_handles)
    kt10_wait.until(EC.element_to_be_clickable((By.ID, "open-new-window"))).click()
    kt10_wait.until(EC.number_of_windows_to_be(len(before) + 1))
    new_handle = (set(kt10_driver.window_handles) - before).pop()
    kt10_driver.switch_to.window(new_handle)
    kt10_wait.until(EC.title_is("KT02 New Window"))
    kt10_shot("05_secondary_window")
    kt10_driver.close()
    kt10_wait.until(EC.number_of_windows_to_be(1))
    kt10_driver.switch_to.window(original)
    assert kt10_driver.title == "KT02 Main Window"
    kt10_shot("06_back_main_window")


@pytest.mark.kt10
@pytest.mark.parametrize("kt10_browser", BROWSERS, indirect=True)
def test_iframe_switch(kt10_driver, kt10_wait, kt10_url, kt10_shot):
    """Переключение в iframe, ввод и возврат в default_content."""
    kt10_driver.get(kt10_url("kt02", "iframe_host.html"))
    kt10_wait.until(EC.title_is("KT02 IFrame Host"))
    frame = kt10_wait.until(EC.presence_of_element_located((By.ID, "demo-frame")))
    kt10_driver.switch_to.frame(frame)
    field = kt10_wait.until(EC.element_to_be_clickable((By.ID, "frame-input")))
    field.clear()
    field.send_keys("KT10 iframe OK")
    kt10_driver.find_element(By.ID, "frame-submit").click()
    result = kt10_wait.until(EC.visibility_of_element_located((By.ID, "frame-result")))
    assert "KT10 iframe OK" in result.text
    kt10_shot("07_inside_iframe")
    kt10_driver.switch_to.default_content()
    host = kt10_wait.until(EC.visibility_of_element_located((By.ID, "host-heading")))
    assert "iframe" in host.text.lower()
    assert kt10_driver.find_elements(By.ID, "frame-input") == []
    kt10_shot("08_default_content")
