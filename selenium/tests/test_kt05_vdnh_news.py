"""КТ 05: функциональные тесты раздела новостей https://vdnh.ru/news/."""

from __future__ import annotations

import re
from urllib.parse import urlparse

import pytest

from pages.vdnh_pages import NEWS_URL, VdnhHomePage, VdnhNewsArticlePage, VdnhNewsListPage


@pytest.mark.kt05
@pytest.mark.smoke
def test_home_page_opens(driver, save_screenshot):
    """Открытие главной страницы VDNH и проверка навигационного контекста."""
    home = VdnhHomePage(driver).open()
    home.safe_screenshot(save_screenshot, "01_home_opened")

    host = urlparse(home.current_url).netloc.lower()
    assert host.endswith("vdnh.ru")
    assert home.title.strip()
    # Site keeps background assets loading; do not require readyState=complete.
    assert urlparse(home.current_url).path in {"", "/"}


@pytest.mark.kt05
@pytest.mark.smoke
def test_news_section_loads(driver, save_screenshot):
    """Раздел /news/ открывается и остаётся в зоне новостей."""
    page = VdnhNewsListPage(driver).open()
    page.safe_screenshot(save_screenshot, "02_news_section_loaded")

    assert "/news" in page.current_url
    assert page.title.strip()


@pytest.mark.kt05
@pytest.mark.smoke
def test_news_heading_visible(driver, save_screenshot):
    """Заголовок раздела новостей отображается."""
    page = VdnhNewsListPage(driver).open()
    heading = page.heading_text()
    page.safe_screenshot(save_screenshot, "03_news_heading")

    assert heading
    assert "новост" in heading.lower()


@pytest.mark.kt05
def test_news_cards_have_meaningful_content(driver, save_screenshot):
    """Карточки новостей присутствуют и содержат осмысленный текст."""
    page = VdnhNewsListPage(driver).open()
    texts = [t for t in page.card_texts() if len(t) >= 20]
    page.safe_screenshot(save_screenshot, "04_news_cards")

    assert page.cards_count() >= 1
    assert len(texts) >= 1, f"Expected meaningful card text, got: {page.card_texts()[:3]!r}"


@pytest.mark.kt05
def test_news_cards_have_distinct_article_links(driver, save_screenshot):
    """У карточек есть различающиеся ссылки на статьи /news/<id>."""
    page = VdnhNewsListPage(driver).open()
    links = page.article_links()
    page.safe_screenshot(save_screenshot, "05_news_card_links")

    assert len(links) >= 2
    assert len(set(links)) == len(links)
    assert all(re.search(r"/news/\d+", href) for href in links)


@pytest.mark.kt05
@pytest.mark.smoke
def test_open_article_from_card(driver, save_screenshot):
    """Переход в карточку новости открывает страницу статьи."""
    list_page = VdnhNewsListPage(driver).open()
    list_url = list_page.current_url
    article = list_page.open_first_article()
    article.safe_screenshot(save_screenshot, "06_article_opened")

    assert re.search(r"/news/\d+", article.current_url)
    assert list_url.rstrip("/") != article.current_url.rstrip("/")


@pytest.mark.kt05
def test_article_heading_and_details(driver, save_screenshot):
    """На странице статьи отображается заголовок и корректный URL детали."""
    article = VdnhNewsListPage(driver).open().open_first_article()
    heading = article.heading_text()
    article.safe_screenshot(save_screenshot, "07_article_heading")

    assert heading
    assert len(heading) >= 10
    assert re.search(r"/news/\d+", article.current_url)
    assert article.title.strip()


@pytest.mark.kt05
def test_navigate_back_to_news_section(driver, save_screenshot):
    """Возврат из статьи в раздел новостей через навигацию сайта."""
    article = VdnhNewsListPage(driver).open().open_first_article()
    news = article.back_to_news()
    news.safe_screenshot(save_screenshot, "08_back_to_news")

    assert "/news" in news.current_url
    assert "новост" in news.heading_text().lower()
    assert news.cards_count() >= 1


@pytest.mark.kt05
def test_show_more_loads_additional_cards(driver, save_screenshot):
    """Кнопка «Показать ещё» подгружает дополнительный контент ленты."""
    page = VdnhNewsListPage(driver).open()
    page.safe_screenshot(save_screenshot, "09_before_show_more")
    try:
        info = page.click_show_more()
    except Exception:
        page.safe_screenshot(save_screenshot, "10_after_show_more_FAILED")
        raise
    page.safe_screenshot(save_screenshot, "10_after_show_more")

    # Accept append (more cards) or batch/URL change that introduces new article links.
    grew_cards = int(info["after_cards"]) > int(info["before_cards"])
    grew_links = int(info["new_links"]) > 0
    url_changed = bool(info["url_changed"])
    assert grew_cards or grew_links or url_changed, (
        f"Expected additional news content after «Показать ещё», got: {info}"
    )


@pytest.mark.kt05
def test_news_logo_and_menu_navigation(driver, save_screenshot):
    """Навигация: новости → главная (логотип) → снова новости (меню)."""
    news = VdnhNewsListPage(driver).open()
    home = news.go_home_via_logo()
    home.safe_screenshot(save_screenshot, "11_news_to_home_logo")
    assert urlparse(home.current_url).netloc.endswith("vdnh.ru")
    assert urlparse(home.current_url).path in {"", "/"}

    news_again = home.open_news_via_navigation()
    news_again.safe_screenshot(save_screenshot, "12_home_to_news_menu")
    assert "/news" in news_again.current_url
    assert news_again.cards_count() >= 1
