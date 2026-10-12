"""Wait until a page is visually ready before taking screenshots."""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


def wait_visually_ready(driver: WebDriver, timeout: float = 20) -> None:
    """Wait for document complete, fonts loaded, and images finished (or broken)."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "return (document.fonts ? document.fonts.status === 'loaded' : true);"
            )
        )
    except Exception:
        pass
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "return Array.from(document.images || []).every("
                "function(img){ return img.complete; });"
            )
        )
    except Exception:
        pass
    # One paint frame after assets settle.
    try:
        driver.execute_script(
            "return new Promise(function(resolve){"
            "requestAnimationFrame(function(){ requestAnimationFrame(resolve); });"
            "});"
        )
    except Exception:
        pass


def chrome_options_for_screenshots(options) -> None:
    """Prefer software-friendly Chrome settings for readable screenshots."""
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-features=PaintHolding")
