"""КТ 02: переключение в iframe и возврат в основной документ."""

from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def iframe_host(driver, wait, fixture_url):
    """Open the local iframe host page."""
    driver.get(fixture_url("kt02", "iframe_host.html"))
    wait.until(EC.presence_of_element_located((By.ID, "host-heading")))
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "demo-frame")))
    driver.switch_to.default_content()
    return driver


@pytest.mark.kt02
def test_switch_into_iframe_interact_and_verify(
    driver, wait, save_screenshot, iframe_host
):
    """Switch into iframe, interact with controls and verify the result."""
    host_status = wait.until(EC.visibility_of_element_located((By.ID, "host-status")))
    assert host_status.text.strip() == "Контекст: основной документ"
    save_screenshot("kt02", "07_iframe_host_before_switch")

    frame = wait.until(EC.presence_of_element_located((By.ID, "demo-frame")))
    driver.switch_to.frame(frame)

    frame_heading = wait.until(
        EC.visibility_of_element_located((By.ID, "frame-heading"))
    )
    assert frame_heading.text.strip() == "Документ внутри iframe"

    field = wait.until(EC.element_to_be_clickable((By.ID, "frame-input")))
    field.clear()
    field.send_keys("КТ02 iframe OK")

    submit = wait.until(EC.element_to_be_clickable((By.ID, "frame-submit")))
    submit.click()

    result = wait.until(EC.visibility_of_element_located((By.ID, "frame-result")))
    wait.until(EC.text_to_be_present_in_element((By.ID, "frame-result"), "КТ02 iframe OK"))
    assert result.text.strip() == "Результат: КТ02 iframe OK"
    save_screenshot("kt02", "08_iframe_interaction_result")


@pytest.mark.kt02
def test_return_to_default_content(driver, wait, save_screenshot, iframe_host):
    """After iframe work, default_content() restores the main document."""
    driver.switch_to.frame(
        wait.until(EC.presence_of_element_located((By.ID, "demo-frame")))
    )
    wait.until(EC.visibility_of_element_located((By.ID, "frame-heading")))
    save_screenshot("kt02", "09_inside_iframe_before_default_content")

    driver.switch_to.default_content()

    host_heading = wait.until(EC.visibility_of_element_located((By.ID, "host-heading")))
    host_footer = wait.until(EC.visibility_of_element_located((By.ID, "host-footer")))
    assert host_heading.text.strip() == "Основной документ с iframe"
    assert host_footer.text.strip() == "Подвал основного документа"
    assert driver.title == "KT02 IFrame Host"

    # Child-document controls are not reachable without switching into the frame again.
    driver.implicitly_wait(0)
    try:
        assert driver.find_elements(By.ID, "frame-input") == []
    finally:
        driver.implicitly_wait(5)

    save_screenshot("kt02", "10_back_to_default_content")
