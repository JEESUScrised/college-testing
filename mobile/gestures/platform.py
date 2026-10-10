"""Cross-platform gesture intent layer.

High-level operations are platform-agnostic. Android executes them via
UiAutomator2 helpers. iOS would plug in an XCUITest implementation — not
available in this lab environment.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from gestures.android_gestures import AndroidGestures, GestureResult

Direction = Literal["up", "down", "left", "right"]


class GesturePort(ABC):
    """Platform-independent gesture contract used by KT09 tests."""

    @abstractmethod
    def swipe(self, direction: Direction, **kwargs) -> GestureResult: ...

    @abstractmethod
    def scroll_until_visible(self, locator: tuple[str, str], **kwargs) -> bool: ...


class AndroidGesturePort(GesturePort):
    def __init__(self, driver: WebDriver) -> None:
        self._impl = AndroidGestures(driver)

    def swipe(self, direction: Direction, **kwargs) -> GestureResult:
        return self._impl.swipe(direction, **kwargs)

    def scroll_until_visible(self, locator: tuple[str, str], **kwargs) -> bool:
        return self._impl.scroll_until_visible(locator, **kwargs)

    @property
    def android(self) -> AndroidGestures:
        return self._impl


class IOSGesturePort(GesturePort):
    """Placeholder for future XCUITest adaptation — not executed in KT09."""

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "iOS GesturePort is not implemented: no XCUITest / iOS device in this environment."
        )

    def swipe(self, direction: Direction, **kwargs) -> GestureResult:
        raise NotImplementedError

    def scroll_until_visible(self, locator: tuple[str, str], **kwargs) -> bool:
        raise NotImplementedError


def create_gesture_port(driver: WebDriver, platform: str = "android") -> GesturePort:
    platform = (platform or "android").lower()
    if platform == "android":
        return AndroidGesturePort(driver)
    if platform in {"ios", "iphone", "ipad"}:
        return IOSGesturePort(driver)
    raise ValueError(f"Unsupported platform for gestures: {platform}")
