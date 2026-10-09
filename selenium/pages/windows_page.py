"""Page Objects for multi-window scenarios (KT02 fixtures)."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WindowsMainPage(BasePage):
    """Main window that opens a secondary browser window."""

    PATH = ("kt02", "windows_main.html")

    MAIN_HEADING = (By.ID, "main-heading")
    MAIN_STATUS = (By.ID, "main-status")
    OPEN_NEW_WINDOW = (By.ID, "open-new-window")

    EXPECTED_TITLE = "KT02 Main Window"
    EXPECTED_HEADING = "Главное окно KT02"

    def open_fixture(self, fixture_url) -> "WindowsMainPage":
        self.open(fixture_url(*self.PATH))
        self.find_visible(self.MAIN_HEADING)
        return self

    def open_secondary_window(self) -> str:
        """Click the link and return the new window handle."""
        original = self.current_window_handle
        before = set(self.window_handles)
        self.click(self.OPEN_NEW_WINDOW)
        self.wait_until_windows_count(len(before) + 1)
        new_handles = set(self.window_handles) - before
        if len(new_handles) != 1:
            raise RuntimeError(f"Expected one new window, got: {new_handles}")
        new_handle = new_handles.pop()
        if new_handle == original:
            raise RuntimeError("New window handle matches the original handle")
        return new_handle

    def heading_text(self) -> str:
        return self.text_of(self.MAIN_HEADING)

    def status_text(self) -> str:
        return self.text_of(self.MAIN_STATUS)


class WindowsSecondaryPage(BasePage):
    """Secondary window opened from WindowsMainPage."""

    NEW_HEADING = (By.ID, "new-heading")
    NEW_BODY = (By.ID, "new-body")

    EXPECTED_TITLE = "KT02 New Window"
    EXPECTED_HEADING = "Содержимое нового окна"

    def switch_to(self, handle: str) -> "WindowsSecondaryPage":
        self.switch_to_window(handle)
        self.wait_until_title_is(self.EXPECTED_TITLE)
        self.find_visible(self.NEW_HEADING)
        return self

    def heading_text(self) -> str:
        return self.text_of(self.NEW_HEADING)

    def body_text(self) -> str:
        return self.text_of(self.NEW_BODY)

    def close_and_return_to(self, original_handle: str) -> None:
        self.close_current_window()
        self.wait_until_windows_count(1)
        self.switch_to_window(original_handle)


# Backwards-friendly alias used in assignment wording.
WindowsPage = WindowsMainPage
