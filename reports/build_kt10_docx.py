"""Generate reports/KT10.docx — historical functional + responsive remediation."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt10"
RESP = SHOTS / "responsive"
OUTPUT = Path(__file__).resolve().parent / "KT10.docx"

HIST = [
    ("TC-10-01", "title/URL", "chrome/firefox", "PASS"),
    ("TC-10-02", "DOM click", "chrome/firefox", "PASS"),
    ("TC-10-03", "form validation", "chrome/firefox", "PASS"),
    ("TC-10-04", "window switch", "chrome/firefox", "PASS"),
    ("TC-10-05", "iframe switch", "chrome/firefox", "PASS"),
]

RESP_CASES = [
    ("TC10-R01", "layout / overflow"),
    ("TC10-R02", "login form"),
    ("TC10-R03", "inventory"),
    ("TC10-R04", "burger menu"),
    ("TC10-R05", "cart"),
    ("TC10-R06", "checkout form"),
]

COMPLIANCE = [
    ("Публичное адаптивное приложение", "Sauce Demo", "PASS"),
    ("Разные браузеры", "Chrome + Firefox", "PASS"),
    ("Desktop/tablet/phone", "1440×900 / 768×1024 / 390×844", "PASS"),
    ("Меню/кнопки/формы", "R02–R06", "PASS"),
    ("Адаптация размеров", "viewport JSONL + screenshots", "PASS"),
    ("Документирование проблем", "overflow: none observed", "PASS"),
    ("Отчёт с рекомендациями", "KT10.docx + docs/kt10/", "PASS"),
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


def add_shot(doc, path: Path, caption: str, w=9.0):
    if not path.is_file():
        add_para(doc, f"[Нет файла: {path.name}]")
        return
    doc.add_picture(str(path), width=Cm(w))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(caption)
    set_run_font(run, size_pt=10)


def add_table(doc, headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    for i, h in enumerate(headers):
        t.rows[0].cells[i].text = h
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = v
    add_para(doc, "")


def build() -> Path:
    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(2)
        s.bottom_margin = Cm(2)
        s.left_margin = Cm(2.5)
        s.right_margin = Cm(1.5)

    add_para(doc, "Дисциплина: Модульное тестирование веб-приложений", center=True)
    add_para(doc, "КТ №10. Кроссбраузерное / адаптивное тестирование", bold=True, center=True)
    add_para(doc, "Дата remediation: 2026-10-10", center=True)

    add_heading(doc, "1. Цель (оригинал презентации)")
    add_para(
        doc,
        "Протестировать публичное адаптивное веб-приложение в разных браузерах "
        "с эмуляцией desktop/tablet/smartphone, проверить меню/формы/раскладку, "
        "зафиксировать проблемы и подготовить отчёт.",
    )

    add_heading(doc, "2. Публичный сайт")
    add_para(doc, "https://www.saucedemo.com/ — login, inventory, menu, cart, checkout.")

    add_heading(doc, "3. Responsive матрица (новое)")
    add_para(doc, "Chrome CDP (tablet/phone) + window resize; Firefox — только resize.")
    add_table(doc, ["ID", "Сценарий"], RESP_CASES)
    add_code(doc, "============================= 6 passed in 42.73s ==============================")
    add_para(doc, "36 evidence rows; horizontal overflow: none observed.")
    for name, cap in [
        ("chrome_phone_r02_login_form.png", "Chrome phone — login"),
        ("firefox_phone_r03_inventory.png", "Firefox phone — inventory"),
        ("chrome_tablet_r04_menu_open.png", "Chrome tablet — menu"),
        ("chrome_desktop_r06_checkout.png", "Chrome desktop — checkout validation"),
    ]:
        add_shot(doc, RESP / name, cap)

    add_heading(doc, "4. Исторический functional suite (сохранён)")
    add_para(doc, "Локальные фикстуры + EventFiringWebDriver listener. Не перезапускался в remediation.")
    add_table(doc, ["ID", "Сценарий", "Browsers", "Status"], HIST)
    add_code(doc, "============================= 10 passed in 52.92s ==============================")
    add_shot(doc, SHOTS / "chrome_01_home_title.png", "Исторический Chrome home", 8)
    add_shot(doc, SHOTS / "firefox_01_home_title.png", "Исторический Firefox home", 8)

    add_heading(doc, "5. Compliance")
    add_table(doc, ["Требование", "Реализация", "Статус"], COMPLIANCE)

    add_heading(doc, "6. Заключение")
    add_para(
        doc,
        "Добавлена responsive матрица Sauce Demo (6/6 PASS, 42.73 с). "
        "Критичных проблем раскладки не обнаружено. Listener/functional suite сохранены.",
    )
    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    for req in ["6 passed in 42.73s", "10 passed in 52.92s", "saucedemo", "Compliance"]:
        if req not in text:
            raise SystemExit(f"missing {req}")
    print(f"OK {path} size={path.stat().st_size}")


if __name__ == "__main__":
    verify(build())
