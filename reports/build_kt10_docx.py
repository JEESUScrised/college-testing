"""Generate reports/KT10.docx from verified cross-browser evidence (Russian)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt10"
OUTPUT = Path(__file__).resolve().parent / "KT10.docx"

RESULTS = [
    ("TC-10-01", "title + URL + capabilities", "chrome", "PASS"),
    ("TC-10-01", "title + URL + capabilities", "firefox", "PASS"),
    ("TC-10-02", "DOM click", "chrome", "PASS"),
    ("TC-10-02", "DOM click", "firefox", "PASS"),
    ("TC-10-03", "form validation", "chrome", "PASS"),
    ("TC-10-03", "form validation", "firefox", "PASS"),
    ("TC-10-04", "window switch", "chrome", "PASS"),
    ("TC-10-04", "window switch", "firefox", "PASS"),
    ("TC-10-05", "iframe switch", "chrome", "PASS"),
    ("TC-10-05", "iframe switch", "firefox", "PASS"),
]

IMAGES = [
    ("chrome_01_home_title.png", "Рисунок 1 — Chrome: home / title"),
    ("firefox_01_home_title.png", "Рисунок 2 — Firefox: home / title"),
    ("chrome_02_dom_click.png", "Рисунок 3 — Chrome: DOM click"),
    ("firefox_02_dom_click.png", "Рисунок 4 — Firefox: DOM click"),
    ("chrome_04_form_valid.png", "Рисунок 5 — Chrome: форма OK"),
    ("firefox_04_form_valid.png", "Рисунок 6 — Firefox: форма OK"),
    ("chrome_05_secondary_window.png", "Рисунок 7 — Chrome: второе окно"),
    ("firefox_05_secondary_window.png", "Рисунок 8 — Firefox: второе окно"),
    ("chrome_07_inside_iframe.png", "Рисунок 9 — Chrome: iframe"),
    ("firefox_07_inside_iframe.png", "Рисунок 10 — Firefox: iframe"),
    (
        "FAIL_chrome_test_intentional_failure_for_screenshot_hook[chrome].png",
        "Рисунок 11 — Controlled FAIL: screenshot-on-failure",
    ),
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


def add_shot(doc, filename, caption):
    path = SHOTS / filename
    if not path.is_file():
        add_para(doc, f"[Нет файла: {filename}]")
        return
    doc.add_picture(str(path), width=Cm(7.5))
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
    add_para(doc, "Студент: _______________________________________", center=True)
    add_para(doc, "")
    add_para(
        doc,
        "КТ №10. Кроссбраузерное тестирование, отчёты и listeners",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата: 2026-10-10", center=True)

    add_heading(doc, "1. Цель")
    add_para(
        doc,
        "Реализовать матрицу Chrome × Firefox (5 сценариев × 2 браузера), "
        "подключить Selenium WebDriver Event Listener и pytest-отчёты "
        "(HTML, JUnit, screenshot-on-failure).",
    )
    add_para(
        doc,
        "Презентация cloud.ithub.ru (КТ10) без авторизации недоступна; "
        "полное соответствие скрытым слайдам не утверждается.",
        bold=True,
    )

    add_heading(doc, "2. Среда")
    add_para(
        doc,
        "Windows 10; Python 3.13.2; Selenium 4.50.0; pytest 8.4.2; "
        "pytest-html 4.2.0; Chrome 155.0.8059.39; Firefox 157.0.1.",
    )
    add_para(
        doc,
        "Код: selenium/crossbrowser/ (отдельный kt10_driver на EventFiringWebDriver; "
        "корневой driver KT01–08 не изменён).",
    )

    add_heading(doc, "3. Listener vs pytest hook")
    add_para(
        doc,
        "Kt10EventListener (AbstractEventListener): before/after navigate и click, "
        "on_exception → selenium/artifacts/kt10/events.jsonl.",
    )
    add_para(
        doc,
        "pytest_runtest_makereport: run_summary.jsonl, PNG при FAIL, extras в HTML-отчёте.",
    )

    add_heading(doc, "4. Команды")
    add_code(
        doc,
        r""".\scripts\diagnose_kt10.ps1
.\scripts\run_kt10.ps1""",
    )

    add_heading(doc, "5. Результаты матрицы 5×2")
    add_para(doc, "Диагностика: DIAGNOSE_PASS. Suite: 10 passed in 52.92s, exit 0.")
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = (
        "ID",
        "Сценарий",
        "Браузер",
        "Статус",
    )
    for row in RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")
    add_code(doc, "============================= 10 passed in 52.92s =============================")
    add_para(
        doc,
        "browser_comparison.json: chrome 5 passed / firefox 5 passed "
        "(версии 155.0.8059.39 и 157.0.1).",
    )

    add_heading(doc, "6. Controlled failure demo")
    add_para(
        doc,
        "Отдельный прогон test_kt10_failure_demo.py: 1 failed (ожидаемо). "
        "Создан FAIL_chrome_….png и запись в failures.jsonl — доказательство "
        "screenshot-on-failure hook.",
    )

    add_heading(doc, "7. Скриншоты")
    for path, caption in IMAGES:
        add_shot(doc, path, caption)

    add_heading(doc, "8. Ограничения")
    add_para(
        doc,
        "Локальные HTML-фикстуры (без публичных сайтов). Edge/Safari не входили "
        "в выбранную матрицу A. Размеры viewport Chrome/Firefox слегка отличаются "
        "(1384×849 vs 1384×907).",
    )

    add_heading(doc, "9. Заключение")
    add_para(
        doc,
        "КТ 10 выполнена: EventFiringWebDriver + listener, pytest HTML/JUnit, "
        "матрица 10/10 PASS, failure demo с скриншотом, отчёт. KT11/KT12 не начинались.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №10. Кроссбраузерное тестирование, отчёты и listeners",
        "10 passed in 52.92s",
        "Event Listener",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise SystemExit(f"DOCX missing: {missing}")
    n_pics = sum(1 for r in doc.part.rels.values() if "image" in r.reltype)
    if n_pics < 10:
        raise SystemExit(f"Expected >=10 images, got {n_pics}")
    print(f"OK {path} images={n_pics} chars={len(text)}")


if __name__ == "__main__":
    out = build()
    verify(out)
