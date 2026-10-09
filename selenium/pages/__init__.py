"""Page Object classes for Selenium control points."""

from pages.base_page import BasePage
from pages.iframe_page import IframePage
from pages.windows_page import WindowsMainPage, WindowsPage, WindowsSecondaryPage

__all__ = [
    "BasePage",
    "IframePage",
    "WindowsMainPage",
    "WindowsPage",
    "WindowsSecondaryPage",
]
