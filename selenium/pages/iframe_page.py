"""Page Object for iframe host/child scenarios (KT02 fixtures)."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class IframePage(BasePage):
    """Host page with an interactive child document inside an iframe."""

    PATH = ("kt02", "iframe_host.html")

    HOST_HEADING = (By.ID, "host-heading")
    HOST_STATUS = (By.ID, "host-status")
    HOST_FOOTER = (By.ID, "host-footer")
    DEMO_FRAME = (By.ID, "demo-frame")

    FRAME_HEADING = (By.ID, "frame-heading")
    FRAME_INPUT = (By.ID, "frame-input")
    FRAME_SUBMIT = (By.ID, "frame-submit")
    FRAME_RESULT = (By.ID, "frame-result")

    EXPECTED_TITLE = "KT02 IFrame Host"
    EXPECTED_HOST_HEADING = "Основной документ с iframe"
    EXPECTED_FRAME_HEADING = "Документ внутри iframe"

    def open_fixture(self, fixture_url) -> "IframePage":
        self.open(fixture_url(*self.PATH))
        self.find_visible(self.HOST_HEADING)
        # Ensure the frame is present, then stay on the host document.
        self.switch_to_frame(self.DEMO_FRAME)
        self.switch_to_default_content()
        return self

    def host_heading_text(self) -> str:
        return self.text_of(self.HOST_HEADING)

    def host_status_text(self) -> str:
        return self.text_of(self.HOST_STATUS)

    def host_footer_text(self) -> str:
        return self.text_of(self.HOST_FOOTER)

    def enter_iframe(self) -> "IframePage":
        self.switch_to_frame(self.DEMO_FRAME)
        self.find_visible(self.FRAME_HEADING)
        return self

    def frame_heading_text(self) -> str:
        return self.text_of(self.FRAME_HEADING)

    def submit_frame_value(self, value: str) -> str:
        """Type a value inside the iframe, submit, and return result text."""
        self.type_text(self.FRAME_INPUT, value)
        self.click(self.FRAME_SUBMIT)
        self.wait.until(EC.text_to_be_present_in_element(self.FRAME_RESULT, value))
        return self.text_of(self.FRAME_RESULT)

    def leave_iframe(self) -> "IframePage":
        self.switch_to_default_content()
        self.find_visible(self.HOST_HEADING)
        return self

    def frame_input_visible_in_current_context(self) -> bool:
        return self.count_elements(self.FRAME_INPUT) > 0
