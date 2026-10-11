"""Generate reports/KT02.docx — historical windows/iframe + public Sauce remediation."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT

from docx_helpers import setup_a4, add_heading, add_para, add_code, add_shot
from report_title import add_title_fields

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


def build() -> Path:
    missing_hist = [n for n, _ in HIST_SHOTS if not (SHOTS / n).is_file()]
    missing_pub = [n for n, _ in PUBLIC_SHOTS if not (PUBLIC / n).is_file()]
    if missing_hist or missing_pub:
        raise FileNotFoundError(f"Missing screenshots: hist={missing_hist} pub={missing_pub}")

    doc = Document()
    setup_a4(doc)

    add_title_fields(doc, add_para)
    add_para(doc, "КТ №2. Тестирование функционала веб-приложения с применением техник тестирования", bold=True, center=True)
    add_para(doc, "Отчёт по контрольной точке (включая remediation 2026-10-10)", center=True)

    add_heading(doc, "О чём КТ №2")
    add_para(
        doc,
        "Здесь уже не просто «открыть сайт», а техники: positive / negative / boundary, "
        "разные локаторы, cookies, window handles. Параллельно оставил старый слой на "
        "локальных HTML — окна/вкладки и iframe. Публичную часть добивал remediation "
        "2026-10-10 на Sauce Demo.",
    )

    add_heading(doc, "Где тестировал")
    add_para(doc, "• Публичный сайт (remediation): https://www.saucedemo.com/")
    add_para(
        doc,
        "• Исторический слой: локальные HTML-фикстуры selenium/fixtures/kt02/ "
        "(окна + iframe)",
    )

    add_heading(doc, "Окружение")
    add_para(doc, "• ОС: Windows 10; Python 3.13.2; pytest 8.4.2; Selenium 4.50; Chrome")
    add_para(doc, "• Page Object для Sauce: selenium/pages/sauce/")
    add_para(doc, "• Ждал элементы через WebDriverWait / EC.*, без лишних sleep")

    add_heading(doc, "Команды, которыми гонял")
    add_code(
        doc,
        """# Публичный Sauce Demo (remediation)
.\\.venv\\Scripts\\python.exe -m pytest selenium\\tests\\test_kt02_sauce_public.py -v --browser=chrome --page-load-strategy=eager

# Исторические окна/iframe
.\\.venv\\Scripts\\python.exe -m pytest selenium\\tests\\test_kt02_windows.py selenium\\tests\\test_kt02_iframe.py -v --browser=chrome""",
    )

    add_heading(doc, "Набор кейсов на Sauce Demo")
    add_para(
        doc,
        "Сначала happy path — login, карточка товара, корзина, checkout. Потом ломаю "
        "вход и checkout пустыми/неверными данными. Boundary — почтовый индекс: пустой "
        "против минимального «1». Отдельно техники: локаторы, cookies, вторая вкладка.",
    )
    add_para(doc, "TC02-P01…P03 — positive: login, product/cart, remove+checkout.")
    add_para(doc, "TC02-N01…N04 — negative: empty user/password, bad credentials, checkout required.")
    add_para(doc, "TC02-B01 — boundary: postal code empty vs minimal «1».")
    add_para(doc, "TC02-T01…T03 — locators (ID/CSS/Name/XPath), cookies, window handles.")

    add_heading(doc, "Цифры с прогонов")
    add_para(doc, "Публичный прогон (2026-10-10):")
    add_code(doc, KT02_PUBLIC)
    add_para(doc, "Исторический прогон окон/iframe (сохранён):")
    add_code(doc, KT02_HIST)
    add_para(
        doc,
        "Итог remediation: 11 passed in 49.34s. Исторический слой: 6 passed in 21.49s. "
        "Оба набора зелёные.",
    )

    add_heading(doc, "Скриншоты старого слоя (окна / iframe)")
    add_para(
        doc,
        "Сначала переключение по window_handles, потом switch_to.frame и возврат через "
        "default_content(). Скриншоты из screenshots/kt02/.",
    )
    for name, caption in HIST_SHOTS:
        add_shot(doc, SHOTS / name, caption)

    add_heading(doc, "Скриншоты Sauce Demo")
    add_para(doc, "Файлы лежат в screenshots/kt02/public/ — positive, negative, boundary и техники.")
    for name, caption in PUBLIC_SHOTS:
        add_shot(doc, PUBLIC / name, caption)

    add_heading(doc, "Заключение")
    add_para(
        doc,
        "На Sauce Demo закрыл техники тестирования: 11 passed in 49.34s, скрины по "
        "каждому типу кейсов. Старые тесты окон/iframe не выкидывал — 6 passed in 21.49s, "
        "они всё ещё показывают switch_to.window и работу с iframe. Для сдачи важны оба "
        "слоя: публичный функционал и исторические handles/frames.",
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
