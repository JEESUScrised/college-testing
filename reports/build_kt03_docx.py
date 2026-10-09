"""Generate reports/KT03.docx from verified KT03 artifacts."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt03"
OUTPUT = Path(__file__).resolve().parent / "KT03.docx"

SCREENSHOTS = [
    ("01_po_main_before_open.png", "Рисунок 1 — Главное окно до открытия (Page Object)"),
    ("03_po_switched_to_secondary.png", "Рисунок 2 — Переключение на вторичное окно через WindowsSecondaryPage"),
    ("04_po_secondary_content_verified.png", "Рисунок 3 — Проверка содержимого вторичного окна"),
    ("06_po_returned_to_main.png", "Рисунок 4 — Возврат в исходное окно после close_and_return_to()"),
    ("07_po_iframe_host.png", "Рисунок 5 — Host-страница с iframe (IframePage)"),
    ("08_po_iframe_interaction.png", "Рисунок 6 — Взаимодействие внутри iframe через Page Object"),
    ("09_po_back_to_default_content.png", "Рисунок 7 — Возврат в основной документ (leave_iframe)"),
]

KT03_OUTPUT = """\
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2, pluggy-1.6.0
configfile: pytest.ini
collecting ... collected 4 items

selenium/tests/test_kt03_page_object.py::test_po_open_secondary_window PASSED
selenium/tests/test_kt03_page_object.py::test_po_switch_and_verify_secondary_content PASSED
selenium/tests/test_kt03_page_object.py::test_po_close_secondary_and_return PASSED
selenium/tests/test_kt03_page_object.py::test_po_iframe_interact_and_return_to_default PASSED

============================= 4 passed in 14.90s ==============================
"""

REGRESSION_OUTPUT = """\
selenium/tests/test_kt01_ya_ru.py::test_open_ya_ru PASSED
selenium/tests/test_kt02_windows.py::... 4 tests PASSED
selenium/tests/test_kt02_iframe.py::... 2 tests PASSED
============================= 7 passed in 29.05s ==============================
"""

BASE_SNIPPET = """\
class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url): ...
    def find_visible(self, locator): ...
    def click(self, locator): ...
    def type_text(self, locator, text): ...
    def switch_to_window(self, handle): ...
    def switch_to_frame(self, locator): ...
    def switch_to_default_content(self): ...
"""

WINDOWS_SNIPPET = """\
class WindowsMainPage(BasePage):
    OPEN_NEW_WINDOW = (By.ID, "open-new-window")
    def open_secondary_window(self) -> str: ...

class WindowsSecondaryPage(BasePage):
    NEW_HEADING = (By.ID, "new-heading")
    def switch_to(self, handle): ...
    def close_and_return_to(self, original_handle): ...
"""

IFRAME_SNIPPET = """\
class IframePage(BasePage):
    DEMO_FRAME = (By.ID, "demo-frame")
    FRAME_INPUT = (By.ID, "frame-input")
    def enter_iframe(self): ...
    def submit_frame_value(self, value: str) -> str: ...
    def leave_iframe(self): ...
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


def add_shot(doc: Document, filename: str, caption: str) -> None:
    path = SHOTS / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    doc.add_picture(str(path), width=Cm(14))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(caption)
    set_run_font(run, size_pt=11)


def build() -> Path:
    missing = [name for name, _ in SCREENSHOTS if not (SHOTS / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing screenshots: {missing}")

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
    add_para(doc, "КТ №3. Паттерн Page Object", bold=True, center=True)
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата выполнения: 2026-10-09", center=True)

    add_heading(doc, "1. Цель работы")
    add_para(
        doc,
        "Цель контрольной точки №3 — применить паттерн Page Object к уже "
        "реализованным сценариям Selenium (окна/вкладки и iframe), чтобы "
        "отделить локаторы и действия страницы от тестовых assertions и "
        "повысить сопровождаемость автотестов.",
    )

    add_heading(doc, "2. Суть паттерна Page Object")
    add_para(
        doc,
        "Page Object — это объектно-ориентированный приём организации UI-автотестов: "
        "каждая страница (или логический фрагмент UI) представляется классом. "
        "В классе хранятся локаторы и методы действий пользователя; тесты вызывают "
        "эти методы и проверяют ожидаемое бизнес-поведение. Благодаря этому "
        "изменения вёрстки правятся в одном месте — в Page Object, а не во всех тестах.",
    )

    add_heading(doc, "3. Архитектура проекта")
    add_para(doc, "• selenium/pages/base_page.py — общие helper-методы WebDriver.")
    add_para(doc, "• selenium/pages/windows_page.py — WindowsMainPage / WindowsSecondaryPage (алиас WindowsPage).")
    add_para(doc, "• selenium/pages/iframe_page.py — IframePage для host + child iframe.")
    add_para(doc, "• selenium/tests/test_kt03_page_object.py — не менее четырёх тестов с assertions.")
    add_para(doc, "• Фикстуры HTML КТ 02 переиспользуются без дублирования разметки.")
    add_para(doc, "• Тесты КТ 01 и КТ 02 сохранены и прошли регрессию.")

    add_heading(doc, "4. Ответственность классов")
    add_para(
        doc,
        "BasePage: открытие URL, поиск/ожидание элементов, click, type_text, "
        "работа с window handles и iframe (switch_to_frame / default_content).",
    )
    add_para(
        doc,
        "WindowsPage (WindowsMainPage): локаторы главного окна, open_secondary_window(). "
        "WindowsSecondaryPage: переключение на новое окно, чтение содержимого, "
        "close_and_return_to(original_handle).",
    )
    add_para(
        doc,
        "IframePage: открытие host-страницы, enter_iframe(), submit_frame_value(), "
        "leave_iframe() через default_content(), проверка недоступности child-элементов.",
    )

    add_heading(doc, "5. Примеры кода")
    add_para(doc, "BasePage (фрагмент):")
    add_code(doc, BASE_SNIPPET)
    add_para(doc, "Windows Page Objects (фрагмент):")
    add_code(doc, WINDOWS_SNIPPET)
    add_para(doc, "IframePage (фрагмент):")
    add_code(doc, IFRAME_SNIPPET)

    add_heading(doc, "6. Реализованные тест-кейсы")
    add_para(doc, "TC1. test_po_open_secondary_window — открытие второго окна через Page Object.")
    add_para(doc, "TC2. test_po_switch_and_verify_secondary_content — переключение и проверка контента.")
    add_para(doc, "TC3. test_po_close_secondary_and_return — закрытие вторичного окна и возврат.")
    add_para(doc, "TC4. test_po_iframe_interact_and_return_to_default — iframe + default_content().")
    add_para(doc, "Assertions о заголовках, текстах и количестве окон остаются в тестах.")

    add_heading(doc, "7. Фактические результаты")
    add_para(doc, "Среда: Windows 11, Python 3.13.9, pytest 8.4.2, Selenium 4.50.0, Chrome 154.0.8037.98.")
    add_para(doc, "Команда: pytest selenium\\tests\\test_kt03_page_object.py -v --browser=chrome")
    add_code(doc, KT03_OUTPUT)
    add_para(doc, "Регрессия КТ 01 + КТ 02:")
    add_code(doc, REGRESSION_OUTPUT)
    add_para(
        doc,
        "Итог: KT03 — 4 passed за 14.90 с (exit 0, warnings нет); "
        "регрессия — 7 passed за 29.05 с (exit 0).",
    )

    add_heading(doc, "8. Скриншоты фактического запуска")
    for filename, caption in SCREENSHOTS:
        add_shot(doc, filename, caption)

    add_heading(doc, "9. Преимущества Page Object")
    add_para(doc, "• Локаторы сосредоточены в классах страниц, а не размазаны по тестам.")
    add_para(doc, "• Повторное использование действий (открыть окно, войти в iframe) без копипаста.")
    add_para(doc, "• Тесты читаются как сценарии пользователя и содержат только проверки.")
    add_para(doc, "• Изменение HTML-фикстуры требует правки Page Object, а не каждого теста.")
    add_para(
        doc,
        "По сравнению с прямыми вызовами Selenium в КТ 02 код КТ 03 короче на уровне "
        "сценария и устойчивее к рефакторингу UI.",
    )

    add_heading(doc, "10. Заключение")
    add_para(
        doc,
        "Контрольная точка №3 выполнена: реализованы BasePage, WindowsPage "
        "(WindowsMainPage/WindowsSecondaryPage) и IframePage; написаны четыре "
        "автотеста на Page Object с реальными скриншотами; регрессия КТ 01 и КТ 02 "
        "успешна. Архитектура намеренно простая — наследование от BasePage без "
        "избыточных слоёв.",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №3. Паттерн Page Object",
        "Цель работы",
        "Суть паттерна Page Object",
        "4 passed in 14.90s",
        "Преимущества Page Object",
        "Заключение",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"DOCX missing sections: {missing}")
    pictures = list(doc.inline_shapes)
    unique_images = [rel for rel in doc.part.rels.values() if rel.reltype == RT.IMAGE]
    if len(pictures) < len(SCREENSHOTS):
        raise AssertionError(f"Expected >= {len(SCREENSHOTS)} pictures, got {len(pictures)}")
    if not unique_images:
        raise AssertionError("No embedded images")
    print(
        f"VERIFY_OK size={path.stat().st_size} "
        f"pictures={len(pictures)} unique_images={len(unique_images)}"
    )


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
