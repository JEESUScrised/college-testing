"""КТ 01: Selenium WebDriver открывает https://ya.ru в Chrome."""

from urllib.parse import urlparse

import pytest


@pytest.mark.kt01
def test_open_ya_ru(driver, save_screenshot):
    """Chrome opens https://ya.ru and navigation succeeds."""
    target = "https://ya.ru"

    driver.get(target)

    current = driver.current_url
    host = urlparse(current).netloc.lower()
    title = (driver.title or "").strip()

    # ya.ru may redirect within the Yandex domain family; require a real loaded page.
    assert host.endswith("ya.ru") or "yandex" in host, (
        f"Unexpected host after navigation: url={current!r}, title={title!r}"
    )
    assert title, f"Page title is empty after opening {target}: url={current!r}"
    assert driver.execute_script("return document.readyState") == "complete", (
        f"Document was not fully loaded: url={current!r}, title={title!r}"
    )

    screenshot_path = save_screenshot("kt01", "ya_ru_opened")
    assert screenshot_path.is_file() and screenshot_path.stat().st_size > 0
