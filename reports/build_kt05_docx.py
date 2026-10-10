"""Generate reports/KT05.docx from verified dual-run KT05 evidence."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt05"
OUTPUT = Path(__file__).resolve().parent / "KT05.docx"

SCREENSHOTS = [
    ("01_home_opened.png", "Рисунок 1 — Главная VDNH (прогон №1)"),
    ("02_news_section_loaded.png", "Рисунок 2 — Раздел /news/ (прогон №1)"),
    ("04_news_cards.png", "Рисунок 3 — Карточки новостей (прогон №1)"),
    ("06_article_opened.png", "Рисунок 4 — Страница статьи (прогон №1)"),
    ("08_back_to_news.png", "Рисунок 5 — Возврат в новости (прогон №1)"),
    ("09_before_show_more.png", "Рисунок 6 — До «Показать еще» (прогон №1, затем FAIL)"),
    ("10_after_show_more.png", "Рисунок 7 — После «Показать еще» (прогон №2, PASS)"),
    ("12_home_to_news_menu.png", "Рисунок 8 — Навигация меню (прогон №1)"),
]

RESULTS = [
    ("TC-05-01", "test_home_page_opens", "PASS", "—"),
    ("TC-05-02", "test_news_section_loads", "PASS", "—"),
    ("TC-05-03", "test_news_heading_visible", "PASS", "—"),
    ("TC-05-04", "test_news_cards_have_meaningful_content", "PASS", "—"),
    ("TC-05-05", "test_news_cards_have_distinct_article_links", "PASS", "—"),
    ("TC-05-06", "test_open_article_from_card", "PASS", "—"),
    ("TC-05-07", "test_article_heading_and_details", "PASS", "—"),
    ("TC-05-08", "test_navigate_back_to_news_section", "PASS", "—"),
    ("TC-05-09", "test_show_more_loads_additional_cards", "FAIL", "PASS"),
    ("TC-05-10", "test_news_logo_and_menu_navigation", "PASS", "—"),
]


def set_run_font(run, size_pt: float = 12, bold: bool = False, name: str = "Times New Roman") -> None:
    run.bold = bold
    run.font.size = Pt(size_pt)
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def add_heading(doc: Document, text: str, level: int = 1) -> None:
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        set_run_font(run, size_pt=14 if level == 1 else 13, bold=True)


def add_para(doc: Document, text: str, *, bold: bool = False, center: bool = False) -> None:
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_run_font(run, bold=bold)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15


def add_code(doc: Document, code: str) -> None:
    for line in code.strip("\n").splitlines():
        p = doc.add_paragraph()
        run = p.add_run(line if line else " ")
        set_run_font(run, size_pt=9, name="Consolas")
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)


def add_shot(doc: Document, filename: str, caption: str) -> None:
    path = SHOTS / filename
    if not path.is_file():
        add_para(doc, f"[Скриншот отсутствует: {filename}]")
        return
    doc.add_picture(str(path), width=Cm(14))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(caption)
    set_run_font(run, size_pt=11)


def build() -> Path:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)

    add_para(doc, "Дисциплина: Модульное тестирование веб-приложений", center=True)
    add_para(doc, "Учебное заведение: ______________________________", center=True)
    add_para(doc, "Студент: _______________________________________", center=True)
    add_para(doc, "Преподаватель: _________________________________", center=True)
    add_para(doc, "Группа: ________________________________________", center=True)
    add_para(doc, "")
    add_para(
        doc,
        "КТ №5. Тестирование функционала сайта и составление тестовой документации",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата: 2026-10-09", center=True)

    add_heading(doc, "1. Цель и требования")
    add_para(
        doc,
        "Выполнить функциональное тестирование публичного раздела новостей ВДНХ "
        "и подготовить тестовую документацию. Референс: "
        "https://github.com/sa-teach/selenium-tests (структура; локаторы сверены с актуальной вёрсткой).",
    )

    add_heading(doc, "2. Обоснование выбора сайта")
    add_para(doc, "URL: https://vdnh.ru/ и https://vdnh.ru/news/")
    add_para(
        doc,
        "Выбран публичный информационный портал ВДНХ: read-only сценарии без регистрации, "
        "реальная лента новостей с подгрузкой, достаточная сложность для Page Object, "
        "этичные ограничения (без нагрузки). Подробнее: docs/kt05/website-selection.md.",
    )
    add_para(
        doc,
        "Бизнес-назначение: информирование посетителей о событиях; критичны доступность "
        "ленты, кликабельность карточек, читаемость статей и подгрузка «Показать ещё».",
    )

    add_heading(doc, "3. Среда и инструменты")
    add_para(doc, "Windows; Python 3.13; pytest 8.4.2; Selenium 4.50.0; Chrome headed.")
    add_para(doc, "pageLoadStrategy=none + DOM waits; запуск без VPN: scripts/run_kt05_no_vpn.ps1.")
    add_para(doc, "Page Object: selenium/pages/vdnh_pages.py; тесты: selenium/tests/test_kt05_vdnh_news.py.")

    add_heading(doc, "4. Методика и критерии")
    add_para(doc, "Black-box — пользовательские сценарии. Gray-box — DOM/CSS/URL/readyState.")
    add_para(doc, "White-box backend: не применим (закрытый сервер VDNH).")
    add_para(doc, "Risk-based: P0 лента/статья; P1 show_more; P2 logo/menu.")
    add_para(doc, "Вход: Chrome, venv, сайт доступен. Выход: ≥8 автотестов, docs/kt05/, DOCX, честные результаты.")
    add_para(doc, "Подробный план: docs/kt05/test-plan.md.")

    add_heading(doc, "5. Трассируемость требований преподавателя")
    add_para(doc, "1) Выбор сайта — website-selection.md / §2. 2) Подходы black/gray/white — §4.")
    add_para(doc, "3) Scope + entry/exit — test-plan.md. 4) Сценарии — test-cases.md + таблица ниже.")
    add_para(doc, "5) Исполнение — §7. 6) Дефекты — §8 / defect-analysis.md (баг сайта не подтверждён).")
    add_para(doc, "7) Рекомендации — §11. 8) Итоговый отчёт — данный DOCX.")

    add_heading(doc, "6. Таблица тест-кейсов (два прогона)")
    add_para(
        doc,
        "Внимание: ниже — результаты двух отдельных запусков. "
        "Единого прогона «10/10 PASS» не было.",
        bold=True,
    )
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = (
        "ID",
        "Автотест",
        "Прогон №1 (полный)",
        "Прогон №2 (show_more)",
    )
    for row in RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")

    add_heading(doc, "7. Фактические результаты прогонов")
    add_para(doc, "Прогон №1 (полный, ~12:57): 9 PASS / 1 FAIL за 98.63 с, exit code 1.")
    add_code(
        doc,
        "FAILED test_show_more_loads_additional_cards\n"
        "TimeoutException in click_show_more() after 35s wait\n"
        "=================== 1 failed, 9 passed in 98.63s ====================",
    )
    add_para(doc, "Прогон №2 (только show_more, ~13:10): 1 PASS за 11.60 с, exit code 0.")
    add_code(
        doc,
        "test_show_more_loads_additional_cards PASSED\n"
        "============================= 1 passed in 11.60s =============================",
    )

    add_heading(doc, "8. Анализ FAIL и follow-up PASS")
    add_para(
        doc,
        "В прогоне №1 кнопка «Показать еще» была на странице; падение — на ожидании "
        "роста контента после клика. Исходная реализация ждала только увеличения "
        "cards_count; возможен stale element после scroll.",
    )
    add_para(
        doc,
        "Перед прогоном №2 Page Object уточнён: перепоиск кнопки; успех = больше карточек "
        "ИЛИ новые article links ИЛИ смена URL. Follow-up PASS и скриншот "
        "10_after_show_more.png (расширенная лента) согласуются с исправлением теста.",
    )
    add_para(
        doc,
        "Остаточная неопределённость: полный suite с новым кодом заново не запускался, "
        "поэтому вклад кратковременной стабильности сайта/сети полностью не исключён. "
        "Дефект сайта не подтверждён. Итог не формулируется как «один прогон 10/10».",
    )

    add_heading(doc, "9. Архитектура Page Object")
    add_para(doc, "VdnhHomePage — главная и переход в новости.")
    add_para(doc, "VdnhNewsListPage — лента, карточки, «Показать еще», логотип.")
    add_para(doc, "VdnhNewsArticlePage — статья и возврат в /news/.")
    add_para(doc, "Локаторы/действия в PO; assertions — в тестах.")

    add_heading(doc, "10. Скриншоты")
    for name, caption in SCREENSHOTS:
        add_shot(doc, name, caption)

    add_heading(doc, "11. Рекомендации")
    add_para(doc, "Продукт: подтверждённых дефектов раздела новостей нет.")
    add_para(
        doc,
        "Процесс: не склеивать полный и follow-up прогоны; составные условия успеха "
        "подгрузки; data-testid на динамических кнопках желательны на стороне сайта; "
        "локаторы перепроверять при смене вёрстки. См. docs/kt05/recommendations.md.",
    )

    add_heading(doc, "12. Заключение")
    add_para(
        doc,
        "КТ 05: 10 функциональных автотестов на https://vdnh.ru/news/, Page Object, "
        "расширенная документация (выбор сайта, методика, дефекты, рекомендации). "
        "Полный прогон: 9 PASS / 1 FAIL. Show_more подтверждён отдельно PASS (11.60 с). "
        "Единого прогона 10/10 не было. Дефект сайта не подтверждён.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №5. Тестирование функционала сайта и составление тестовой документации",
        "9 PASS / 1 FAIL",
        "1 passed in 11.60s",
        "Единого прогона «10/10 PASS» не было",
        "https://vdnh.ru/news/",
        "Обоснование выбора сайта",
        "Рекомендации",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    if len(doc.tables) < 1:
        raise AssertionError("Expected results table")
    pictures = list(doc.inline_shapes)
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    if len(pictures) < 6:
        raise AssertionError(f"pictures={len(pictures)}")
    if not images:
        raise AssertionError("no images")
    print(f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} unique={len(images)} tables={len(doc.tables)}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
