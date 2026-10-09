"""Page Objects for https://vdnh.ru (КТ 05 functional tests)."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage

BASE_URL = "https://vdnh.ru"
NEWS_URL = f"{BASE_URL}/news/"


class VdnhBasePage(BasePage):
    """Shared helpers for the heavy VDNH public site."""

    LOGO_HOME = (By.CSS_SELECTOR, "a[href='https://vdnh.ru/'], a[href='/'], header a.navbar-brand")
    NAV_NEWS = (By.CSS_SELECTOR, "a[href='https://vdnh.ru/news'], a[href='https://vdnh.ru/news/'], a[href='/news'], a[href='/news/']")
    COOKIE_BUTTONS = (
        By.CSS_SELECTOR,
        ".cookie button, .cookie__wrap button, .cookie .btn, button[class*='cookie']",
    )

    def __init__(self, driver, timeout: int = 25) -> None:
        super().__init__(driver, timeout=timeout)

    def open_url(self, url: str) -> None:
        try:
            self.driver.get(url)
        except TimeoutException:
            # page_load_strategy=none/eager may still raise on slow assets; DOM can be usable.
            pass
        WebDriverWait(self.driver, self.wait._timeout).until(
            lambda d: urlparse(d.current_url).netloc.endswith("vdnh.ru")
        )
        self.dismiss_overlays()

    def dismiss_overlays(self) -> None:
        self.driver.implicitly_wait(0)
        try:
            for btn in self.driver.find_elements(*self.COOKIE_BUTTONS):
                if not btn.is_displayed():
                    continue
                text = (btn.text or "").strip().lower()
                if text and not any(token in text for token in ("ок", "ok", "приня", "соглас", "accept")):
                    continue
                try:
                    btn.click()
                    break
                except WebDriverException:
                    continue
        finally:
            self.driver.implicitly_wait(5)

    def safe_screenshot(self, save_screenshot, name: str) -> None:
        try:
            save_screenshot("kt05", name)
        except WebDriverException:
            # Renderer can hang on screenshots while background assets keep loading.
            pass


class VdnhHomePage(VdnhBasePage):
    """Main site entry point."""

    def open(self) -> "VdnhHomePage":
        self.open_url(f"{BASE_URL}/")
        WebDriverWait(self.driver, self.wait._timeout).until(
            lambda d: bool((d.title or "").strip())
        )
        return self

    def open_news_via_navigation(self) -> "VdnhNewsListPage":
        self.dismiss_overlays()
        candidates = self.driver.find_elements(*self.NAV_NEWS)
        for link in candidates:
            href = (link.get_attribute("href") or "").rstrip("/")
            if href.endswith("/news"):
                try:
                    link.click()
                    break
                except (ElementClickInterceptedException, WebDriverException):
                    self.driver.get(NEWS_URL)
                    break
        else:
            self.driver.get(NEWS_URL)
        return VdnhNewsListPage(self.driver).wait_loaded()


class VdnhNewsListPage(VdnhBasePage):
    """News listing at /news/."""

    HEADING = (By.CSS_SELECTOR, "h1")
    # Exact card root only — do not match nested *.news__card-main__date badges.
    CARDS = (By.CSS_SELECTOR, "div.news__card-main, article.news__card-main, .card.news__card-main")
    # UI text uses both «ещё» and «еще»; control may be button or link-styled control.
    SHOW_MORE = (
        By.XPATH,
        "//*[self::button or self::a or @role='button']"
        "[contains(normalize-space(.), 'Показать ещё') or "
        "contains(normalize-space(.), 'Показать еще') or "
        "contains(normalize-space(.), 'Показать ещ')]",
    )

    def open(self) -> "VdnhNewsListPage":
        self.open_url(NEWS_URL)
        return self.wait_loaded()

    def wait_loaded(self) -> "VdnhNewsListPage":
        self.dismiss_overlays()
        WebDriverWait(self.driver, self.wait._timeout).until(
            lambda d: any((e.text or "").strip() for e in d.find_elements(*self.HEADING))
        )
        WebDriverWait(self.driver, self.wait._timeout).until(
            EC.presence_of_element_located(self.CARDS)
        )
        return self

    def heading_text(self) -> str:
        for element in self.driver.find_elements(*self.HEADING):
            text = (element.text or "").strip()
            if text:
                return text
        raise AssertionError("H1 heading not found on /news/")

    def cards(self):
        return [c for c in self.driver.find_elements(*self.CARDS) if c.is_displayed()]

    def cards_count(self) -> int:
        return len(self.cards())

    def card_texts(self) -> list[str]:
        return [(c.text or "").strip() for c in self.cards() if (c.text or "").strip()]

    def article_links(self) -> list[str]:
        links: list[str] = []
        for anchor in self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/news/']"):
            href = (anchor.get_attribute("href") or "").strip()
            if not href or href.rstrip("/").endswith("/news"):
                continue
            if re.search(r"/news/\d+", href):
                links.append(href.split("#")[0].rstrip("/") + "/")
        # Preserve order, unique
        unique: list[str] = []
        for href in links:
            if href not in unique:
                unique.append(href)
        return unique

    def open_first_article(self) -> "VdnhNewsArticlePage":
        links = self.article_links()
        if not links:
            raise AssertionError("No article links found on /news/")
        target = links[0]
        try:
            self.driver.get(target)
        except TimeoutException:
            pass
        return VdnhNewsArticlePage(self.driver).wait_loaded()

    def click_show_more(self) -> dict[str, object]:
        """Click «Показать ещё» and wait until additional news content appears.

        The public site may append cards, replace the batch, or change the URL.
        Success is any of: more visible cards, new article links, or URL change.
        Returns a small diagnostic dict for assertions/logging.
        """
        self.dismiss_overlays()
        before_cards = self.cards_count()
        before_links = set(self.article_links())
        before_url = self.current_url

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Re-locate immediately before clicking to avoid a stale element after scroll.
        button = WebDriverWait(self.driver, self.wait._timeout).until(
            EC.presence_of_element_located(self.SHOW_MORE)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        button = self.driver.find_element(*self.SHOW_MORE)
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.SHOW_MORE))
            button.click()
        except (ElementClickInterceptedException, TimeoutException, WebDriverException):
            button = self.driver.find_element(*self.SHOW_MORE)
            self.driver.execute_script("arguments[0].click();", button)

        def _content_grew(driver) -> bool:
            self.driver.implicitly_wait(0)
            try:
                cards = len([c for c in driver.find_elements(*self.CARDS) if c.is_displayed()])
                links = set()
                for anchor in driver.find_elements(By.CSS_SELECTOR, "a[href*='/news/']"):
                    href = (anchor.get_attribute("href") or "").strip()
                    if href and re.search(r"/news/\d+", href) and not href.rstrip("/").endswith("/news"):
                        links.add(href.split("#")[0].rstrip("/") + "/")
                url = driver.current_url
                return (
                    cards > before_cards
                    or len(links - before_links) > 0
                    or url != before_url
                )
            finally:
                self.driver.implicitly_wait(5)

        try:
            WebDriverWait(self.driver, 35).until(_content_grew)
        except TimeoutException as exc:
            after_cards = self.cards_count()
            after_links = set(self.article_links())
            raise TimeoutException(
                "«Показать ещё» did not expose additional news content within 35s. "
                f"cards {before_cards}->{after_cards}; "
                f"article_links {len(before_links)}->{len(after_links)} "
                f"(new={len(after_links - before_links)}); "
                f"url before={before_url!r} after={self.current_url!r}"
            ) from exc

        after_cards = self.cards_count()
        after_links = set(self.article_links())
        return {
            "before_cards": before_cards,
            "after_cards": after_cards,
            "before_links": len(before_links),
            "after_links": len(after_links),
            "new_links": len(after_links - before_links),
            "url_changed": self.current_url != before_url,
        }

    def go_home_via_logo(self) -> VdnhHomePage:
        self.dismiss_overlays()
        for link in self.driver.find_elements(*self.LOGO_HOME):
            href = (link.get_attribute("href") or "").rstrip("/")
            if href.endswith("vdnh.ru"):
                try:
                    link.click()
                except WebDriverException:
                    self.open_url(f"{BASE_URL}/")
                break
        else:
            self.open_url(f"{BASE_URL}/")
        home = VdnhHomePage(self.driver)
        WebDriverWait(self.driver, self.wait._timeout).until(
            lambda d: urlparse(d.current_url).path in {"", "/"}
        )
        return home


class VdnhNewsArticlePage(VdnhBasePage):
    """Individual news article page."""

    HEADING = (By.CSS_SELECTOR, "h1")

    def wait_loaded(self) -> "VdnhNewsArticlePage":
        self.dismiss_overlays()
        WebDriverWait(self.driver, self.wait._timeout).until(
            lambda d: bool(re.search(r"/news/\d+", d.current_url))
        )
        WebDriverWait(self.driver, self.wait._timeout).until(
            lambda d: any((e.text or "").strip() for e in d.find_elements(*self.HEADING))
        )
        return self

    def heading_text(self) -> str:
        for element in self.driver.find_elements(*self.HEADING):
            text = (element.text or "").strip()
            if text:
                return text
        raise AssertionError("Article H1 not found")

    def back_to_news(self) -> VdnhNewsListPage:
        self.dismiss_overlays()
        for link in self.driver.find_elements(*self.NAV_NEWS):
            href = (link.get_attribute("href") or "").rstrip("/")
            if href.endswith("/news"):
                try:
                    link.click()
                    break
                except WebDriverException:
                    self.open_url(NEWS_URL)
                    break
        else:
            self.open_url(NEWS_URL)
        return VdnhNewsListPage(self.driver).wait_loaded()
