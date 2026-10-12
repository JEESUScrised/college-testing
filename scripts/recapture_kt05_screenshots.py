"""Recapture KT05 VDNH screenshots with images enabled and visual settle."""

from __future__ import annotations

import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "selenium"))
from screenshot_ready import chrome_options_for_screenshots, wait_visually_ready  # noqa: E402

OUT = ROOT / "screenshots" / "kt05"
BASE = "https://vdnh.ru"


def _shot(drv, name: str) -> None:
    path = OUT / name
    wait_visually_ready(drv, timeout=30)
    assert drv.save_screenshot(str(path)), path
    print(f"  {name} {path.stat().st_size}")


def main() -> None:
    opts = Options()
    opts.add_argument("--window-size=1400,1000")
    opts.page_load_strategy = "eager"
    chrome_options_for_screenshots(opts)
    # Do NOT disable images — needed for honest media evidence.
    drv = webdriver.Chrome(options=opts)
    wait = WebDriverWait(drv, 35)
    try:
        drv.set_page_load_timeout(40)
        try:
            drv.get(BASE + "/")
        except Exception:
            pass
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        _shot(drv, "01_home_opened.png")

        try:
            drv.get(BASE + "/news/")
        except Exception:
            pass
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        _shot(drv, "02_news_section_loaded.png")
        _shot(drv, "03_news_heading.png")
        _shot(drv, "04_news_cards.png")
        _shot(drv, "05_news_card_links.png")

        # Open first article link if present
        links = drv.find_elements(By.CSS_SELECTOR, "a[href*='/news/']")
        article = None
        for a in links:
            href = a.get_attribute("href") or ""
            if href.rstrip("/").count("/") >= 4 and "/news/" in href and href.rstrip("/") != (BASE + "/news").rstrip("/"):
                article = a
                break
        if article:
            drv.execute_script("arguments[0].click();", article)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            _shot(drv, "06_article_opened.png")
            _shot(drv, "07_article_heading.png")
            drv.back()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            _shot(drv, "08_back_to_news.png")

        _shot(drv, "09_before_show_more.png")
        # Try show more
        for xp in (
            "//*[contains(text(),'Показать еще')]",
            "//*[contains(text(),'Показать ещё')]",
            "//button[contains(.,'Показать')]",
        ):
            els = drv.find_elements(By.XPATH, xp)
            if els:
                try:
                    drv.execute_script("arguments[0].click();", els[0])
                    wait_visually_ready(drv, timeout=20)
                except Exception:
                    pass
                break
        _shot(drv, "10_after_show_more.png")
        _shot(drv, "11_news_to_home_logo.png")
        _shot(drv, "12_home_to_news_menu.png")
    finally:
        drv.quit()
    print("DONE KT05")


if __name__ == "__main__":
    main()
