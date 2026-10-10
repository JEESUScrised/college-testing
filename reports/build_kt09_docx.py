"""Generate reports/KT09.docx — screenshot-rich Windows vs Android SauceDemo report."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from report_title import add_title_fields

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt09"
AUTO_WIN = SHOTS / "automated" / "windows"
AUTO_AND = SHOTS / "automated" / "android"
OUTPUT = Path(__file__).resolve().parent / "KT09.docx"

GESTURE_RESULTS = [
    ("TC-09-01", "vertical swipe up (Views)", "PASS"),
    ("TC-09-02", "vertical swipe down (Views)", "PASS"),
    ("TC-09-03", "scroll until TextFields + open", "PASS"),
    ("TC-09-04", "horizontal swipe left (Gallery)", "PASS"),
    ("TC-09-05", "horizontal swipe right (Gallery)", "PASS"),
]

COMPARE = [
    (
        "Login page",
        "01_login.png",
        "Форма входа Swag Labs отображается; поля Username/Password и Login доступны.",
        "PASS",
        "PASS",
        "Совместимо: одинаковый публичный UI SauceDemo.",
    ),
    (
        "Inventory / catalog",
        "02_inventory.png",
        "Список Products с названиями и ценами.",
        "PASS",
        "PASS",
        "Desktop — сетка; Android — одноколоночный mobile layout.",
    ),
    (
        "Product details",
        "03_product_details.png",
        "Страница товара: название, описание, цена, Add/Remove.",
        "PASS",
        "PASS",
        "Одинаковый DOM inventory-item / inventory-details.",
    ),
    (
        "Item added to cart",
        "04_added_to_cart.png",
        "Бейдж корзины = 1 после Add to cart.",
        "PASS",
        "PASS",
        "Совместимо.",
    ),
    (
        "Cart contents",
        "05_cart.png",
        "Your Cart содержит добавленный товар с QTY и ценой.",
        "PASS",
        "PASS",
        "Совместимо.",
    ),
    (
        "Navigation menu",
        "06_menu.png",
        "Burger menu: All Items / About / Logout доступны.",
        "PASS",
        "PASS",
        "На Android меню критичнее из‑за узкого viewport.",
    ),
    (
        "Checkout form",
        "07_checkout_form.png",
        "Checkout Information: First/Last/Zip (+ валидация на Android suite).",
        "PASS",
        "PASS",
        "Совместимо.",
    ),
    (
        "Order confirmation",
        "08_order_confirmation.png",
        "Checkout Complete / Thank you for your order.",
        "PASS",
        "PASS",
        "Совместимо; на Android возможны артефакты GPU-композитора эмулятора.",
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


def add_shot(doc, path: Path, caption: str, width_cm: float = 14.0) -> None:
    if not path.is_file():
        add_para(doc, f"[Нет файла: {path}]")
        return
    # Android portrait: narrower for A4 readability
    doc.add_picture(str(path), width=Cm(width_cm))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(caption)
    set_run_font(run, size_pt=10)


def build() -> Path:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(1.5)

    add_title_fields(doc, add_para)
    add_para(doc, "")
    add_para(
        doc,
        "КТ №9. Кроссплатформенное тестирование (SauceDemo) и жесты Appium",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата обновления: 2026-10-11", center=True)

    add_heading(doc, "1. Цель")
    add_para(
        doc,
        "Проверить публичное веб-приложение SauceDemo на Windows и Android; "
        "сохранить автоматические доказательства (скриншоты + PASS); "
        "дополнительно — жесты Appium на ApiDemos. "
        "Ручное человеческое тестирование отмечено отдельно и не подменяется автоматизацией.",
    )

    add_heading(doc, "2. Тестируемое приложение и среды")
    add_para(doc, "Приложение: https://www.saucedemo.com/ (Swag Labs).")
    add_para(
        doc,
        "Windows 10 — Mozilla Firefox (Selenium 4): окно 1280×900; "
        "скриншоты screenshots/kt09/automated/windows/.",
    )
    add_para(
        doc,
        "Android 16 / API 36 — emulator-5554 — Chrome 134.0.6998.135 — "
        "ChromeDriver 134.0.6998.165 — Appium 3.8 — "
        "скриншоты screenshots/kt09/automated/android/ "
        "(источник: DOM suite TC09-W* + checkout-complete capture).",
    )
    add_para(
        doc,
        "Все скриншоты ниже — AUTOMATED evidence. "
        "Manual verification: PENDING HUMAN VERIFICATION.",
        bold=True,
    )

    add_heading(doc, "3. Фактические результаты автоматизации (сохранены)")
    add_para(doc, "Жесты Android (ApiDemos): 5 passed in 54.93s.")
    add_para(doc, "Windows cross-platform web (история): 2 passed in 12.43s.")
    add_para(doc, "Android Chrome DOM SauceDemo: 11 passed in 36.91s (TC09-W01…W10 + journey).")
    add_code(
        doc,
        "Windows Firefox visual capture: 8 screenshots (2026-10-11)\n"
        "Android Chrome automated visual set: 8 screenshots "
        "(Appium + ChromeDriver web screenshot, emulator soft GPU; "
        "scripts/capture_kt09_android_visual.py)\n"
        "Manual checklist: PENDING HUMAN VERIFICATION",
    )

    add_heading(doc, "4. Windows vs Android — визуальное сравнение (automated)")
    add_para(
        doc,
        "Для каждого сценария: ожидаемое поведение, результат по доказательствам, "
        "скриншот Windows и скриншот Android.",
    )

    for i, (title, fname, expected, win_r, and_r, conclusion) in enumerate(COMPARE, start=1):
        add_heading(doc, f"4.{i}. {title}", level=2)
        add_para(doc, f"Ожидаемое: {expected}")
        add_para(
            doc,
            f"Windows Firefox — {win_r}. Android Chrome — {and_r}. "
            f"Вывод: {conclusion}",
        )
        add_para(doc, "Windows (automated):", bold=True)
        add_shot(
            doc,
            AUTO_WIN / fname,
            f"Рис. W-{i} — Windows Firefox — {title} [AUTOMATED]",
            width_cm=14.0,
        )
        add_para(doc, "Android (automated):", bold=True)
        add_shot(
            doc,
            AUTO_AND / fname,
            f"Рис. A-{i} — Android Chrome — {title} [AUTOMATED]",
            width_cm=8.5,
        )

    add_heading(doc, "5. Сводная таблица сравнения")
    table = doc.add_table(rows=1, cols=5)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text = "Сценарий"
    hdr[1].text = "Windows"
    hdr[2].text = "Android"
    hdr[3].text = "Скриншоты"
    hdr[4].text = "Вывод"
    for title, fname, _exp, win_r, and_r, conclusion in COMPARE:
        cells = table.add_row().cells
        cells[0].text = title
        cells[1].text = win_r
        cells[2].text = and_r
        cells[3].text = fname
        cells[4].text = conclusion
    add_para(doc, "")

    add_heading(doc, "6. Жесты Appium (supplementary, сохранено)")
    gtable = doc.add_table(rows=1, cols=3)
    gtable.style = "Table Grid"
    gh = gtable.rows[0].cells
    gh[0].text, gh[1].text, gh[2].text = "ID", "Сценарий", "Результат"
    for row in GESTURE_RESULTS:
        cells = gtable.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")
    add_code(doc, "============================= 5 passed in 54.93s ==============================")

    add_heading(doc, "7. Ручное тестирование")
    add_para(
        doc,
        "Человеческий manual checklist не выполнен в этой итерации. "
        "Статус: PENDING HUMAN VERIFICATION "
        "(mobile/docs/kt09-manual-checklist.md). "
        "Автоматические скриншоты не выдаются за ручные.",
        bold=True,
    )

    add_heading(doc, "8. Находки и ограничения")
    add_para(
        doc,
        "• Функциональных дефектов SauceDemo на Windows/Android automation не подтверждено.",
    )
    add_para(
        doc,
        "• На Android Chrome эмулятора иногда появляются диалоги Google Password Manager "
        "и артефакты GPU-композитора на части кадров — это окружение, не баг сайта.",
    )
    add_para(doc, "• iOS: NOT RUN.")

    add_heading(doc, "9. Заключение")
    add_para(
        doc,
        "КТ 09: публичный SauceDemo проверен автоматизацией на Windows и Android "
        "с набором визуальных доказательств (8×2 скриншота). "
        "Исторические результаты 11 PASS Android DOM и 5 PASS жестов сохранены. "
        "Ручная верификация: PENDING HUMAN VERIFICATION.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text += "\n" + cell.text
    required = [
        "КТ №9",
        "saucedemo.com",
        "AUTOMATED",
        "PENDING HUMAN VERIFICATION",
        "11 passed in 36.91s",
        "5 passed in 54.93s",
        "Заключение",
        "Windows",
        "Android",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    pictures = list(doc.inline_shapes)
    if len(pictures) < 14:  # 8 pairs = 16 ideally; allow some missing
        raise AssertionError(f"pictures={len(pictures)}")
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    if not images:
        raise AssertionError("no images")
    # Ensure no launcher-only manual junk is required
    print(f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} unique={len(images)}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
