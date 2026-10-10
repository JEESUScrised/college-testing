"""Modern Appium gesture helpers for Android (no TouchAction).

Uses:
- mobile: swipeGesture
- mobile: scrollGesture
- optional W3C pointer actions as a fallback path
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webelement import WebElement


@dataclass(frozen=True)
class GestureResult:
    direction: str
    moved: bool
    before_signature: tuple[str, ...]
    after_signature: tuple[str, ...]
    detail: str = ""


class AndroidGestures:
    """Platform-specific gesture executor for Android / UiAutomator2."""

    # Keep clear of system gesture/nav edges
    EDGE_PADDING_RATIO = 0.12

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def window_size(self) -> dict[str, int]:
        size = self.driver.get_window_size()
        return {"width": int(size["width"]), "height": int(size["height"])}

    def _safe_rect(self, element: WebElement | None = None) -> dict[str, int]:
        if element is not None:
            rect = element.rect
            return {
                "left": int(rect["x"]),
                "top": int(rect["y"]),
                "width": int(rect["width"]),
                "height": int(rect["height"]),
            }
        size = self.window_size()
        pad_x = int(size["width"] * self.EDGE_PADDING_RATIO)
        pad_y = int(size["height"] * self.EDGE_PADDING_RATIO)
        return {
            "left": pad_x,
            "top": pad_y,
            "width": size["width"] - 2 * pad_x,
            "height": size["height"] - 2 * pad_y,
        }

    def visible_text_signature(self) -> tuple[str, ...]:
        """Collect currently visible list/item labels for movement assertions."""
        self.driver.implicitly_wait(0)
        try:
            nodes = self.driver.find_elements(
                AppiumBy.XPATH,
                "//android.widget.TextView[@resource-id='android:id/text1' or @resource-id='android:id/title']",
            )
            labels: list[str] = []
            for node in nodes:
                try:
                    if not node.is_displayed():
                        continue
                    text = (node.text or node.get_attribute("content-desc") or "").strip()
                    if text:
                        labels.append(text)
                except Exception:
                    continue
            if labels:
                return tuple(labels)
            # Fallback: any displayed TextView with non-empty text
            nodes = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            for node in nodes[:40]:
                try:
                    if node.is_displayed():
                        text = (node.text or "").strip()
                        if text:
                            labels.append(text)
                except Exception:
                    continue
            return tuple(labels)
        finally:
            self.driver.implicitly_wait(0)

    def is_displayed(self, locator: tuple[str, str]) -> bool:
        self.driver.implicitly_wait(0)
        try:
            els = self.driver.find_elements(*locator)
            return bool(els) and els[0].is_displayed()
        except Exception:
            return False
        finally:
            self.driver.implicitly_wait(0)

    def swipe(
        self,
        direction: str,
        *,
        element: WebElement | None = None,
        percent: float = 0.65,
        speed: int = 1200,
    ) -> GestureResult:
        """Swipe using mobile: swipeGesture within a safe area."""
        direction = direction.lower().strip()
        if direction not in {"up", "down", "left", "right"}:
            raise ValueError(f"Unsupported swipe direction: {direction}")

        before = self.visible_text_signature()
        params: dict[str, Any] = {
            "direction": direction,
            "percent": percent,
            "speed": speed,
        }
        if element is not None:
            # Prefer element-scoped swipe for nested scrollables (e.g. Gallery)
            params["elementId"] = element.id
            area = dict(element.rect)
        else:
            area = self._safe_rect(None)
            params.update(area)
        self.driver.execute_script("mobile: swipeGesture", params)
        after = self.visible_text_signature()
        moved = before != after
        return GestureResult(
            direction=direction,
            moved=moved,
            before_signature=before,
            after_signature=after,
            detail=f"swipeGesture percent={percent} target={area}",
        )

    def swipe_up(self, **kwargs: Any) -> GestureResult:
        return self.swipe("up", **kwargs)

    def swipe_down(self, **kwargs: Any) -> GestureResult:
        return self.swipe("down", **kwargs)

    def swipe_left(self, **kwargs: Any) -> GestureResult:
        return self.swipe("left", **kwargs)

    def swipe_right(self, **kwargs: Any) -> GestureResult:
        return self.swipe("right", **kwargs)

    def scroll(
        self,
        direction: str,
        *,
        element: WebElement | None = None,
        percent: float = 0.7,
        speed: int = 1100,
    ) -> GestureResult:
        """Scroll using mobile: scrollGesture."""
        direction = direction.lower().strip()
        if direction not in {"up", "down", "left", "right"}:
            raise ValueError(f"Unsupported scroll direction: {direction}")
        before = self.visible_text_signature()
        area = self._safe_rect(element)
        can_scroll = self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "left": area["left"],
                "top": area["top"],
                "width": area["width"],
                "height": area["height"],
                "direction": direction,
                "percent": percent,
                "speed": speed,
            },
        )
        after = self.visible_text_signature()
        moved = before != after or bool(can_scroll)
        return GestureResult(
            direction=direction,
            moved=moved,
            before_signature=before,
            after_signature=after,
            detail=f"scrollGesture canScroll={can_scroll} area={area}",
        )

    def scroll_until_visible(
        self,
        locator: tuple[str, str],
        *,
        direction: str = "down",
        max_swipes: int = 8,
        element: WebElement | None = None,
    ) -> bool:
        """Swipe/scroll until locator is displayed or attempts exhausted."""
        if self.is_displayed(locator):
            return True
        for _ in range(max_swipes):
            # Appium direction "down" reveals content below (finger moves up).
            self.swipe(direction if direction in {"up", "down", "left", "right"} else "up", element=element)
            if self.is_displayed(locator):
                return True
        return self.is_displayed(locator)

    def w3c_swipe(
        self,
        direction: str,
        *,
        element: WebElement | None = None,
        duration_ms: int = 400,
    ) -> GestureResult:
        """Fallback W3C pointer swipe based on element/window geometry."""
        direction = direction.lower().strip()
        area = self._safe_rect(element)
        cx = area["left"] + area["width"] // 2
        cy = area["top"] + area["height"] // 2
        dx = int(area["width"] * 0.35)
        dy = int(area["height"] * 0.35)
        start = (cx, cy)
        if direction == "up":
            end = (cx, cy - dy)
        elif direction == "down":
            end = (cx, cy + dy)
        elif direction == "left":
            end = (cx - dx, cy)
        elif direction == "right":
            end = (cx + dx, cy)
        else:
            raise ValueError(direction)

        before = self.visible_text_signature()
        finger = PointerInput("touch", "finger")
        actions = ActionBuilder(self.driver, mouse=finger)
        actions.pointer_action.move_to_location(*start)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(duration_ms / 1000)
        actions.pointer_action.move_to_location(*end)
        actions.pointer_action.release()
        actions.perform()
        after = self.visible_text_signature()
        return GestureResult(
            direction=direction,
            moved=before != after,
            before_signature=before,
            after_signature=after,
            detail=f"w3c pointer {start}->{end}",
        )
