"""Page Objects for ApiDemos screens used by KT09 gesture tests."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.api_demos_pages import ApiDemosHomePage
from pages.base_page import BaseMobilePage


class ViewsMenuPage(BaseMobilePage):
    """ApiDemos → Views scrollable menu."""

    LIST = (AppiumBy.ID, "android:id/list")

    def wait_loaded(self) -> "ViewsMenuPage":
        self.find(self.LIST)
        # Animation is typically near the top of Views
        self.find_visible(self.by_accessibility_id("Animation"))
        return self

    def open_from_home(self) -> "ViewsMenuPage":
        home = ApiDemosHomePage(self.driver).wait_loaded()
        home.click_menu_item("Views")
        return self.wait_loaded()

    def visible_items(self) -> list[str]:
        items = self.driver.find_elements(
            AppiumBy.XPATH, "//android.widget.TextView[@resource-id='android:id/text1']"
        )
        return [(i.text or "").strip() for i in items if (i.text or "").strip()]

    def list_element(self):
        return self.find(self.LIST)


class GalleryPhotosPage(BaseMobilePage):
    """Views → Gallery → 1. Photos (horizontal Gallery widget)."""

    GALLERY = (AppiumBy.ID, "io.appium.android.apis:id/gallery")
    TITLE = (AppiumBy.XPATH, "//*[contains(@text,'Gallery')]")

    def open_from_home(self) -> "GalleryPhotosPage":
        home = ApiDemosHomePage(self.driver).wait_loaded()
        home.click_menu_item("Views")
        # Gallery may require scroll in Views list
        home.click_menu_item("Gallery")
        home.click_menu_item("1. Photos")
        self.find(self.GALLERY)
        return self

    def gallery(self):
        return self.find(self.GALLERY)

    def image_position_signature(self) -> tuple[tuple[int, int], ...]:
        gal = self.gallery()
        images = gal.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView")
        return tuple((int(img.rect["x"]), int(img.rect["width"])) for img in images)
