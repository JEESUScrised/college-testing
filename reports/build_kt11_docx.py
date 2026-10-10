"""Generate reports/KT11.docx from verified Robot Framework evidence (Russian)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt11"
OUTPUT = Path(__file__).resolve().parent / "KT11.docx"

RESULTS = [
    ("TC-11-01", "Page opens / title", "PASS", "2.74"),
    ("TC-11-02", "Navigation link", "PASS", "2.80"),
    ("TC-11-03", "Valid form submit", "PASS", "2.81"),
    ("TC-11-04", "Invalid form rejected", "PASS", "2.81"),
    ("TC-11-05", "Checkbox select/deselect", "PASS", "2.78"),
    ("TC-11-06", "Radio button selection", "PASS", "2.79"),
    ("TC-11-07", "Dropdown selection", "PASS", "2.80"),
    ("TC-11-08", "Iframe interact + return", "PASS", "2.82"),
    ("TC-11-09", "New tab switch + return", "PASS", "2.88"),
    ("TC-11-10", "Dynamic UI update", "PASS", "2.77"),
]

IMAGES = [
    ("01_home_title.png", "Рисунок 1 — Home / title"),
    ("02_navigation_register.png", "Рисунок 2 — Навигация на регистрацию"),
    ("03_form_valid.png", "Рисунок 3 — Валидная форма"),
    ("04_form_invalid.png", "Рисунок 4 — Ошибка валидации"),
    ("05_checkbox.png", "Рисунок 5 — Checkbox"),
    ("06_radio.png", "Рисунок 6 — Radio"),
    ("07_dropdown.png", "Рисунок 7 — Dropdown"),
    ("08_iframe.png", "Рисунок 8 — IFrame host после взаимодействия"),
    ("09_secondary_tab.png", "Рисунок 9 — Вторичная вкладка"),
    ("10_dynamic_update.png", "Рисунок 10 — Динамический статус"),
    ("11_robot_report.png", "Рисунок 11 — Robot report.html (10 passed)"),
    ("12_robot_log.png", "Рисунок 12 — Robot log.html"),
]

ROBOT_SAMPLE = r"""*** Test Cases ***
TC-11-03 Valid Form Submission Succeeds
    [Tags]    KT11    form    positive
    Open Registration Page
    Submit Registration Form    Анна Тестова    anna.kt11@example.com
    Verify Form Accepted    Анна Тестова    anna.kt11@example.com
    Capture Scenario Screenshot    03_form_valid"""


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
    width = Cm(14) if filename.startswith("11_") or filename.startswith("12_") else Cm(7.5)
    doc.add_picture(str(path), width=width)
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
        "КТ №11. Автоматизированное тестирование с Robot Framework",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата: 2026-10-10", center=True)

    add_heading(doc, "1. Цель задания")
    add_para(
        doc,
        "Реализовать ровно 10 различимых тест-кейсов на native синтаксисе Robot Framework "
        "с SeleniumLibrary, keyword-driven архитектурой, локальным приложением и "
        "стандартными отчётами Robot Framework.",
    )
    add_para(
        doc,
        "Презентация cloud.ithub.ru (КТ11) без авторизации недоступна; "
        "полное соответствие скрытым слайдам не утверждается.",
        bold=True,
    )

    add_heading(doc, "2. Обзор Robot Framework")
    add_para(
        doc,
        "Robot Framework — keyword-driven фреймворк приёмочного тестирования. "
        "Тесты описываются в файлах .robot секциями Settings, Variables, Test Cases, Keywords. "
        "Отчёты: output.xml (машиночитаемый), log.html (детальный лог), report.html (сводка).",
    )

    add_heading(doc, "3. SeleniumLibrary и keyword-driven архитектура")
    add_para(
        doc,
        "SeleniumLibrary предоставляет ключевые слова браузерной автоматизации "
        "(Open Browser, Click Element, Select Frame, Switch Window и др.). "
        "Высокоуровневые ключевые слова вынесены в resources: "
        "Open Test Application, Submit Registration Form, Verify Form Validation, "
        "Open Secondary Tab, Return To Main Page, Interact Inside Demo Iframe.",
    )
    add_para(
        doc,
        "Python-хелпер FixtureServer.py используется только для локального HTTP "
        "(динамический порт) — логика проверок остаётся в .robot файлах.",
    )

    add_heading(doc, "4. Среда и версии")
    add_para(
        doc,
        "Windows 10; Python 3.13.2; Robot Framework 7.5; SeleniumLibrary 6.9.0; "
        "Selenium 4.50.0; Chrome. Зависимости: robot/requirements.txt "
        "(selenium зафиксирован на 4.50.0, чтобы не ломать KT01–KT10).",
    )

    add_heading(doc, "5. Тестовое приложение")
    add_para(
        doc,
        "Локальные HTML-страницы robot/fixtures/: навигация, форма, checkbox/radio/dropdown, "
        "iframe, вторичная вкладка, динамический статус. Без публичных сайтов и VPN.",
    )

    add_heading(doc, "6. Таблица из 10 тест-кейсов")
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = (
        "ID",
        "Сценарий",
        "Статус",
        "с",
    )
    for row in RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")

    add_heading(doc, "7. Пример кода .robot")
    add_code(doc, ROBOT_SAMPLE)

    add_heading(doc, "8. Переиспользуемые keywords и resources")
    add_para(
        doc,
        "common.resource — Suite Bootstrap/Teardown, Open/Close Test Application, "
        "скриншоты. pages.resource — страничные keywords (формы, iframe, вкладки, dynamic).",
    )
    add_code(
        doc,
        r""".\scripts\run_kt11.ps1
.\.venv\Scripts\python.exe -m robot --outputdir robot\artifacts\kt11 robot\tests\kt11.robot""",
    )

    add_heading(doc, "9. Фактические результаты")
    add_para(doc, "Dry-run: 10 tests discovered. Diagnostic TC-11-01: PASS.")
    add_para(doc, "Полный suite: 10 tests, 10 passed, 0 failed; elapsed ≈ 28.39 с.")
    add_code(doc, "10 tests, 10 passed, 0 failed\nSUITE PASS elapsed= 28.389725")
    add_para(
        doc,
        "Артефакты: output.xml, log.html, report.html, xunit.xml в robot/artifacts/kt11/.",
    )

    add_heading(doc, "10–11. Скриншоты браузера и отчётов Robot")
    for path, caption in IMAGES:
        add_shot(doc, path, caption)

    add_heading(doc, "12. Заключение")
    add_para(
        doc,
        "КТ 11 выполнена: 10 native Robot-тестов, SeleniumLibrary, keyword-driven resources, "
        "локальные фикстуры, suite 10/10 PASS (~28.4 с), отчёты Robot и DOCX. "
        "KT12 не начиналась.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №11. Автоматизированное тестирование с Robot Framework",
        "10 tests, 10 passed, 0 failed",
        "SeleniumLibrary",
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
