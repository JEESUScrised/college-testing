"""Generate reports/KT08.docx — Pillow history + public site + Allure compliance."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt08"
BASELINES = ROOT / "selenium" / "baselines" / "kt08"
ARTIFACTS = ROOT / "selenium" / "artifacts" / "kt08"
OUTPUT = Path(__file__).resolve().parent / "KT08.docx"

PILLOW_RESULTS = [
    ("TC-08-01", "match baseline", "0.0000%", "PASS"),
    ("TC-08-02", "text/color change", "1.1082%", "PASS"),
    ("TC-08-03", "layout shift", "5.0647%", "PASS"),
    ("TC-08-04", "significant diff", "99.8457%", "PASS"),
    ("TC-08-05", "dimension mismatch", "n/a", "PASS"),
]

PUBLIC_RESULTS = [
    ("TC-08-P01", "Login page / branding / form", "PASS"),
    ("TC-08-P02", "Inventory after login", "PASS"),
    ("TC-08-P03", "Sort dropdown", "PASS"),
    ("TC-08-P04", "Add to cart / badge", "PASS"),
]

COMPLIANCE = [
    ("1. Выбрать публичное веб-приложение и UI-элементы", "Sauce Demo (saucedemo.com); login, inventory, dropdown, cart", "docs + public_*.png", "PASS"),
    ("2. Настроить Selenium + test framework", "pytest + Selenium 4.50 Chrome viewport 1400×1000", "conftest / run_kt08.ps1", "PASS"),
    ("3. Интегрировать Allure", "allure-pytest 2.16.2 + CLI 2.37.0", "allure-results / allure-report", "PASS"),
    ("4. Автотесты скриншотов UI/страниц", "4 public + 5 Pillow tests", "test_kt08_*.py", "PASS"),
    ("5. Выполнить тесты и собрать скриншоты", "Full 9 passed in 34.64s", "screenshots/kt08/", "PASS"),
    ("6. Сгенерировать Allure HTML со скриншотами", "allure generate → index.html; PNG в шагах", "allure-report + allure_*.png", "PASS"),
    ("7. Анализ UI + отчёт с выводами", "Этот DOCX + docs/kt08/", "reports/KT08.docx", "PASS"),
]


def set_run_font(run, size_pt=12, bold=False, name="Times New Roman"):
    run.bold = bold
    run.font.size = Pt(size_pt)
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        set_run_font(run, size_pt=14 if level == 1 else 13, bold=True)


def add_para(doc, text, *, bold=False, center=False):
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_run_font(run, bold=bold)
    p.paragraph_format.space_after = Pt(6)


def add_code(doc, code):
    for line in code.strip("\n").splitlines():
        p = doc.add_paragraph()
        run = p.add_run(line if line else " ")
        set_run_font(run, size_pt=9, name="Consolas")
        p.paragraph_format.space_after = Pt(0)


def add_shot(doc, path: Path, caption: str, width_cm=11.0):
    if not path.is_file():
        add_para(doc, f"[Нет файла: {path}]")
        return
    doc.add_picture(str(path), width=Cm(width_cm))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(caption)
    set_run_font(run, size_pt=11)


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")


def build() -> Path:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)

    add_para(doc, "Дисциплина: Модульное тестирование веб-приложений", center=True)
    add_para(doc, "Студент: _______________________________________", center=True)
    add_para(doc, "")
    add_para(
        doc,
        "КТ №8. Скриншотное тестирование веб-приложений и Allure",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке (compliance remediation)", center=True)
    add_para(doc, "Дата: 2026-10-10", center=True)

    add_heading(doc, "1. Цель задания (из презентации преподавателя)")
    add_para(
        doc,
        "Изучить скриншотное тестирование веб-приложений и интегрировать результаты "
        "тестирования с Allure reporting: выбрать публичный сайт, настроить Selenium, "
        "подключить Allure, выполнить скриншотные автотесты, собрать отчёт Allure и "
        "подготовить аналитический отчёт.",
    )

    add_heading(doc, "2. Публичный сайт и обоснование")
    add_para(
        doc,
        "Выбран https://www.saucedemo.com/ — публичное demo-приложение Swag Labs "
        "(login, каталог, dropdown сортировки, корзина).",
    )
    add_para(
        doc,
        "Кандидат https://the-internet.herokuapp.com/ недоступен для Chrome automation "
        "на данной машине: после get() DOM остаётся пустым (challenge/bot script). "
        "Отклонение задокументировано; localhost не подменял требование публичного сайта.",
        bold=True,
    )

    add_heading(doc, "3. Сценарии Selenium на публичном сайте")
    add_table(doc, ["ID", "Сценарий", "Статус"], PUBLIC_RESULTS)
    add_para(
        doc,
        "Файл: selenium/tests/test_kt08_public_allure.py. Viewport 1400×1000, "
        "pageLoadStrategy=eager, явные ожидания без Sleep.",
    )

    add_heading(doc, "4. Архитектура Allure")
    add_para(
        doc,
        "allure-pytest 2.16.2 пишет результаты в selenium/artifacts/kt08/allure-results/. "
        "Allure CLI 2.37.0 (Java 21) генерирует HTML: allure generate … -o allure-report. "
        "В тестах: @allure.title/description/severity/step + allure.attach.file(PNG).",
    )
    add_code(
        doc,
        r""".\scripts\run_kt08.ps1 -Mode Full
# → allure-results + allure-report\index.html""",
    )

    add_heading(doc, "5. Скриншоты публичного сайта")
    for name, cap in [
        ("public_01_login_page.png", "Рис. P1 — Login page"),
        ("public_02_inventory.png", "Рис. P2 — Inventory / Products"),
        ("public_03_sort_dropdown.png", "Рис. P3 — Sort dropdown (Z to A)"),
        ("public_04_add_to_cart.png", "Рис. P4 — Add to cart / badge=1"),
    ]:
        add_shot(doc, SHOTS / name, cap)

    add_heading(doc, "6. Allure attachments и HTML-отчёт")
    add_para(
        doc,
        "В allure-results: 9 test result JSON; PNG/text attachments во вложенных steps "
        "(проверено парсером). HTML-отчёт открывается (title «Allure Report»).",
    )
    add_shot(doc, SHOTS / "allure_01_overview.png", "Рис. A1 — Allure overview")
    add_shot(doc, SHOTS / "allure_02_suites.png", "Рис. A2 — Allure suites/navigation")

    add_heading(doc, "7. Результаты выполнения")
    add_para(doc, "DiagnosticPublic: 1 passed in 3.84s.")
    add_para(doc, "Public only: 4 passed in 21.27s.")
    add_code(doc, "============================= 9 passed in 34.64s ==============================")
    add_para(
        doc,
        "Full suite (Pillow + Public), 2026-10-10. "
        "Лог: pytest_kt08_20261010_144813.log.",
    )

    add_heading(doc, "8. Анализ UI Sauce Demo")
    add_para(
        doc,
        "Login page: явные поля user-name/password и подсказка accepted usernames — удобно "
        "для обучения. Inventory: стабильные data-test атрибуты; сортировка через native "
        "<select>. Корзина обновляет badge. Наблюдение: после select React перерисовывает "
        "DOM (нужен re-find); the-internet.herokuapp.com непригоден под automation здесь.",
    )
    add_para(
        doc,
        "Рекомендации: для скриншотных тестов предпочитать сайты без bot-challenge; "
        "фиксировать viewport; крепить PNG в Allure steps, а не только в файловую систему.",
    )

    add_heading(doc, "9. Сохранённый контур Pillow (исторический)")
    add_para(
        doc,
        "Локальные HTML-фикстуры + compare.py. Исторический прогон: 5 passed in 13.71s "
        "(2026-10-09). В remediation Pillow-тесты сохранены и прошли в Full suite; "
        "diff/overlay также аттачатся в Allure.",
    )
    add_table(doc, ["ID", "Сценарий", "Diff%", "Статус"], PILLOW_RESULTS)
    add_shot(doc, BASELINES / "home_baseline.png", "Рис. L1 — Approved baseline", 9)
    add_shot(doc, SHOTS / "01_home_actual.png", "Рис. L2 — Actual match", 9)
    if (ARTIFACTS / "02_text_color_overlay.png").is_file():
        add_shot(doc, ARTIFACTS / "02_text_color_overlay.png", "Рис. L3 — Overlay text/color", 9)

    add_heading(doc, "10. Compliance checklist (7 требований)")
    add_table(doc, ["Требование", "Реализация", "Доказательство", "Статус"], COMPLIANCE)

    add_heading(doc, "11. Заключение")
    add_para(
        doc,
        "КТ 08 приведена в соответствие с оригинальной презентацией: публичный сайт, "
        "Allure HTML со скриншотами, 9/9 PASS в полном прогоне. Локальный Pillow-контур "
        "сохранён как дополнительная детерминированная проверка.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №8. Скриншотное тестирование веб-приложений и Allure",
        "9 passed in 34.64s",
        "saucedemo.com",
        "Compliance checklist",
        "5 passed in 13.71s",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise SystemExit(f"DOCX missing: {missing}")
    n_pics = sum(1 for r in doc.part.rels.values() if "image" in r.reltype)
    print(f"OK {path} size={path.stat().st_size} images={n_pics} chars={len(text)}")


if __name__ == "__main__":
    out = build()
    verify(out)
