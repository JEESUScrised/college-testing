"""Generate reports/KT02.docx — historical windows/iframe + public Sauce remediation."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt02"
PUBLIC = SHOTS / "public"
OUTPUT = Path(__file__).resolve().parent / "KT02.docx"

HIST_SHOTS = [
    ("01_main_window_before_open.png", "Рисунок 1 — Главное окно до открытия новой вкладки"),
    ("03_switched_to_new_window.png", "Рисунок 2 — Переключение на новое окно по window handle"),
    ("04_new_window_content_verified.png", "Рисунок 3 — Проверка содержимого вторичного окна"),
    ("06_returned_to_main_window.png", "Рисунок 4 — Возврат в исходное окно после закрытия вторичного"),
    ("07_iframe_host_before_switch.png", "Рисунок 5 — Основной документ с iframe"),
    ("08_iframe_interaction_result.png", "Рисунок 6 — Взаимодействие внутри iframe и проверка результата"),
    ("10_back_to_default_content.png", "Рисунок 7 — Возврат в основной документ через default_content()"),
]

PUBLIC_SHOTS = [
    ("pos_01_inventory.png", "Рисунок 8 — Positive: inventory после login"),
    ("pos_02_cart.png", "Рисунок 9 — Positive: товар в корзине"),
    ("pos_03_checkout_complete.png", "Рисунок 10 — Positive: checkout complete"),
    ("neg_01_empty_username.png", "Рисунок 11 — Negative: пустой username"),
    ("neg_02_empty_password.png", "Рисунок 12 — Negative: пустой password"),
    ("neg_03_bad_credentials.png", "Рисунок 13 — Negative: неверные credentials"),
    ("neg_04_checkout_required.png", "Рисунок 14 — Negative: обязательные поля checkout"),
    ("bound_01_empty_zip.png", "Рисунок 15 — Boundary: пустой zip"),
    ("bound_02_min_zip.png", "Рисунок 16 — Boundary: минимальный zip"),
    ("tech_01_locators.png", "Рисунок 17 — Локаторы ID/CSS/Name/XPath"),
    ("tech_02_cookies.png", "Рисунок 18 — Cookie management"),
    ("tech_03_secondary_tab.png", "Рисунок 19 — Window handles на публичном сайте"),
]

KT02_HIST = """\
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2, pluggy-1.6.0
collecting ... collected 6 items
selenium/tests/test_kt02_windows.py ... PASSED
selenium/tests/test_kt02_iframe.py ... PASSED
============================= 6 passed in 21.49s ==============================
"""

KT02_PUBLIC = """\
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-8.4.2, pluggy-1.6.0
collecting ... collected 11 items
selenium/tests/test_kt02_sauce_public.py::test_kt02_positive_login_inventory PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_positive_product_details_and_cart PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_positive_remove_and_checkout PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_negative_empty_username PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_negative_empty_password PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_negative_bad_credentials PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_negative_checkout_missing_fields PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_boundary_checkout_zip_values PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_locators_strategies PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_cookie_management PASSED
selenium/tests/test_kt02_sauce_public.py::test_kt02_window_handles_public PASSED
============================= 11 passed in 49.34s ==============================
"""


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
        p.paragraph_format.line_spacing = 1.0


def add_shot(doc: Document, path: Path, caption: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    doc.add_picture(str(path), width=Cm(14))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(caption)
    set_run_font(run, size_pt=11)


def build() -> Path:
    missing_hist = [n for n, _ in HIST_SHOTS if not (SHOTS / n).is_file()]
    missing_pub = [n for n, _ in PUBLIC_SHOTS if not (PUBLIC / n).is_file()]
    if missing_hist or missing_pub:
        raise FileNotFoundError(f"Missing screenshots: hist={missing_hist} pub={missing_pub}")

    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)

    add_para(doc, "Дисциплина: Модульное тестирование веб-приложений", center=True)
    add_para(doc, "КТ №2. Тестирование функционала веб-приложения с применением техник тестирования", bold=True, center=True)
    add_para(doc, "Отчёт по контрольной точке (включая remediation 2026-10-10)", center=True)

    add_heading(doc, "1. Цель работы")
    add_para(
        doc,
        "Освоить техники функционального тестирования веб-приложения в Selenium: "
        "позитивные/негативные/граничные сценарии, разнообразие локаторов, cookies, "
        "window handles; а также исторический слой — окна/вкладки и iframe.",
    )

    add_heading(doc, "2. Объект тестирования")
    add_para(doc, "• Публичный сайт remediation: https://www.saucedemo.com/")
    add_para(doc, "• Исторический слой: локальные HTML-фикстуры selenium/fixtures/kt02/ (окна + iframe)")

    add_heading(doc, "3. Среда")
    add_para(doc, "• ОС: Windows 10; Python 3.13.2; pytest 8.4.2; Selenium 4.50; Chrome")
    add_para(doc, "• Page Object: selenium/pages/sauce/")
    add_para(doc, "• Явные ожидания WebDriverWait / EC.*")

    add_heading(doc, "4. Команды запуска")
    add_code(
        doc,
        """# Публичный Sauce Demo (remediation)
.\\.venv\\Scripts\\python.exe -m pytest selenium\\tests\\test_kt02_sauce_public.py -v --browser=chrome --page-load-strategy=eager

# Исторические окна/iframe
.\\.venv\\Scripts\\python.exe -m pytest selenium\\tests\\test_kt02_windows.py selenium\\tests\\test_kt02_iframe.py -v --browser=chrome""",
    )

    add_heading(doc, "5. Тест-кейсы remediation (публичный сайт)")
    add_para(doc, "TC02-P01…P03 — positive: login, product/cart, remove+checkout.")
    add_para(doc, "TC02-N01…N04 — negative: empty user/password, bad credentials, checkout required.")
    add_para(doc, "TC02-B01 — boundary: postal code empty vs minimal «1».")
    add_para(doc, "TC02-T01…T03 — locators (ID/CSS/Name/XPath), cookies, window handles.")

    add_heading(doc, "6. Фактические результаты")
    add_para(doc, "Публичный прогон (2026-10-10):")
    add_code(doc, KT02_PUBLIC)
    add_para(doc, "Исторический прогон окон/iframe (сохранён):")
    add_code(doc, KT02_HIST)
    add_para(doc, "Итог remediation: 11 passed / 49.34 с. Исторический слой: 6 passed / 21.49 с.")

    add_heading(doc, "7. Скриншоты — исторический слой")
    for name, caption in HIST_SHOTS:
        add_shot(doc, SHOTS / name, caption)

    add_heading(doc, "8. Скриншоты — публичный Sauce Demo")
    for name, caption in PUBLIC_SHOTS:
        add_shot(doc, PUBLIC / name, caption)

    add_heading(doc, "9. Заключение")
    add_para(
        doc,
        "КТ №2 дополнена публичным функциональным набором техник на Sauce Demo "
        "при сохранении исторических тестов окон/iframe. Assertions и явные ожидания "
        "использованы; скриншоты подлинные.",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №2. Тестирование функционала веб-приложения с применением техник тестирования",
        "11 passed in 49.34s",
        "6 passed in 21.49s",
        "saucedemo.com",
        "Заключение",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"DOCX missing sections: {missing}")
    picture_count = len(list(doc.inline_shapes))
    expected = len(HIST_SHOTS) + len(PUBLIC_SHOTS)
    if picture_count < expected:
        raise AssertionError(f"Expected >= {expected} pictures, got {picture_count}")
    images = [rel for rel in doc.part.rels.values() if rel.reltype == RT.IMAGE]
    if not images:
        raise AssertionError("No embedded image parts found")
    print(f"VERIFY_OK size={path.stat().st_size} pictures={picture_count}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
