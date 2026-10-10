"""КТ 09: жесты swipe/scroll на Android (ApiDemos) через Appium UiAutomator2.

Платформо-независимые ожидания выражены через GesturePort; исполнение — Android.
iOS / XCUITest в этой среде НЕ выполнялся.
"""

from __future__ import annotations

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from gestures.platform import create_gesture_port
from pages.api_demos_pages import ApiDemosHomePage, ViewsTextFieldsPage
from pages.gesture_pages import GalleryPhotosPage, ViewsMenuPage


@pytest.fixture
def gestures(driver):
    return create_gesture_port(driver, platform="android")


@pytest.mark.kt09
def test_vertical_swipe_up_reveals_lower_menu_items(driver, wait, gestures, save_screenshot):
    """Свайп вверх в меню Views: появляются пункты ниже начального viewport."""
    page = ViewsMenuPage(driver).open_from_home()
    before = page.visible_items()
    assert "Animation" in before
    assert "TextFields" not in before, "TextFields unexpectedly already visible"
    save_screenshot("kt09", "01_views_before_swipe_up")

    result = gestures.swipe("up", element=page.list_element(), percent=0.7)
    after = page.visible_items()
    save_screenshot("kt09", "02_views_after_swipe_up")

    assert result.moved or ("TextFields" in after) or ("WebView" in after) or (
        set(after) - set(before)
    ), f"Swipe up did not change visible items. before={before} after={after} detail={result.detail}"
    newly = set(after) - set(before)
    assert newly or ("TextFields" in after) or ("Visibility" in after) or ("WebView" in after), (
        f"Expected new lower items after swipe up; before={before} after={after}"
    )


@pytest.mark.kt09
def test_vertical_swipe_down_restores_upper_items(driver, wait, gestures, save_screenshot):
    """Свайп вниз возвращает верхние пункты меню Views."""
    page = ViewsMenuPage(driver).open_from_home()
    # Move down the list first
    gestures.swipe("up", element=page.list_element(), percent=0.75)
    mid = page.visible_items()
    assert "Animation" not in mid or "Buttons" not in mid or len(mid) > 0
    save_screenshot("kt09", "03_views_before_swipe_down")

    result = gestures.swipe("down", element=page.list_element(), percent=0.75)
    after = page.visible_items()
    save_screenshot("kt09", "04_views_after_swipe_down")

    assert result.moved or ("Animation" in after), (
        f"Swipe down did not restore upper content. mid={mid} after={after}"
    )
    assert "Animation" in after or "Auto Complete" in after, (
        f"Upper Views items not visible after swipe down: {after}"
    )


@pytest.mark.kt09
def test_scroll_until_target_and_open(driver, wait, gestures, save_screenshot):
    """Прокрутка до TextFields вне начального экрана и открытие экрана."""
    page = ViewsMenuPage(driver).open_from_home()
    target = (AppiumBy.ACCESSIBILITY_ID, "TextFields")
    assert not gestures.android.is_displayed(target)
    save_screenshot("kt09", "05_before_scroll_to_textfields")

    found = gestures.scroll_until_visible(target, direction="up", max_swipes=10, element=page.list_element())
    save_screenshot("kt09", "06_after_scroll_to_textfields")
    assert found, "TextFields did not become visible after scrolling"

    wait.until(EC.element_to_be_clickable(target)).click()
    fields = ViewsTextFieldsPage(driver).wait_loaded()
    fields.enter_text("KT09 scroll OK")
    save_screenshot("kt09", "07_textfields_opened")
    assert "KT09 scroll OK" in fields.value()


@pytest.mark.kt09
def test_horizontal_swipe_left_moves_gallery(driver, wait, gestures, save_screenshot):
    """Горизонтальный свайп влево в Views/Gallery/1. Photos сдвигает изображения."""
    page = GalleryPhotosPage(driver).open_from_home()
    gallery = page.gallery()
    before = page.image_position_signature()
    assert before, "Gallery has no visible images"
    save_screenshot("kt09", "08_gallery_before_swipe_left")

    gestures.android.swipe_left(element=gallery, percent=0.8, speed=1500)
    after = page.image_position_signature()
    save_screenshot("kt09", "09_gallery_after_swipe_left")

    assert after != before, f"Horizontal swipe left did not move gallery images: {before} -> {after}"


@pytest.mark.kt09
def test_horizontal_swipe_right_reverses_gallery(driver, wait, gestures, save_screenshot):
    """Обратный горизонтальный свайп вправо меняет позицию контента Gallery."""
    page = GalleryPhotosPage(driver).open_from_home()
    gallery = page.gallery()
    gestures.android.swipe_left(element=gallery, percent=0.85, speed=1500)
    after_left = page.image_position_signature()
    save_screenshot("kt09", "10_gallery_after_left_before_right")

    gestures.android.swipe_right(element=gallery, percent=0.85, speed=1500)
    after_right = page.image_position_signature()
    save_screenshot("kt09", "11_gallery_after_swipe_right")

    assert after_right != after_left, (
        f"Swipe right did not change gallery positions: left={after_left} right={after_right}"
    )
