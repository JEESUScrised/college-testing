"""Generate reports/KT01.docx from verified KT01 artifacts."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT = ROOT / "screenshots" / "kt01" / "ya_ru_opened.png"
OUTPUT = Path(__file__).resolve().parent / "KT01.docx"

TEST_OUTPUT = """\
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2, pluggy-1.6.0 -- ...\\.venv\\Scripts\\python.exe
cachedir: .pytest_cache
rootdir: ...\\college-testing
configfile: pytest.ini
collecting ... collected 1 item

selenium/tests/test_kt01_ya_ru.py::test_open_ya_ru PASSED                [100%]

============================== 1 passed in 4.99s ==============================
"""

FIXTURE_CODE = """\
def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", choices=("chrome", "firefox"))

@pytest.fixture
def driver(browser_name):
    options = ChromeOptions()
    options.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=options)
    drv.set_page_load_timeout(30)
    drv.implicitly_wait(5)
    drv.set_script_timeout(30)
    try:
        yield drv
    finally:
        drv.quit()
"""

TEST_CODE = """\
@pytest.mark.kt01
def test_open_ya_ru(driver, save_screenshot):
    target = "https://ya.ru"
    driver.get(target)
    current = driver.current_url
    host = urlparse(current).netloc.lower()
    title = (driver.title or "").strip()
    assert host.endswith("ya.ru") or "yandex" in host
    assert title
    assert driver.execute_script("return document.readyState") == "complete"
    screenshot_path = save_screenshot("kt01", "ya_ru_opened")
    assert screenshot_path.is_file() and screenshot_path.stat().st_size > 0
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


def build() -> Path:
    if not SCREENSHOT.is_file():
        raise FileNotFoundError(f"Screenshot not found: {SCREENSHOT}")

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
    add_para(doc, "КТ №1. Запуск и работа с WebDriver в Selenium", bold=True, center=True)
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата выполнения: 2026-10-09", center=True)

    add_heading(doc, "1. Цель работы")
    add_para(
        doc,
        "Цель контрольной точки №1 — освоить базовый запуск Selenium WebDriver 4 "
        "в браузере Google Chrome, открыть сайт https://ya.ru и подтвердить успешную "
        "навигацию проверяемыми утверждениями (assertions).",
    )

    add_heading(doc, "2. Требования задания")
    add_para(doc, "Согласно постановке задания (КТ 01, 5 баллов):")
    add_para(doc, "• реализовать автотест на Python с использованием pytest и Selenium 4;")
    add_para(doc, "• запустить Google Chrome через WebDriver;")
    add_para(doc, "• открыть адрес https://ya.ru;")
    add_para(doc, "• проверить успешность перехода осмысленными assertions;")
    add_para(doc, "• зафиксировать результат реальным скриншотом и отчётом.")

    add_heading(doc, "3. Программное обеспечение и тестовая среда")
    add_para(doc, "• Операционная система: Windows 11 (10.0.26100)")
    add_para(doc, "• Интерпретатор: Python 3.13.9")
    add_para(doc, "• Фреймворк тестов: pytest 8.4.2")
    add_para(doc, "• Библиотека автоматизации: Selenium 4.50.0")
    add_para(doc, "• Браузер: Google Chrome 154.0.8037.98")
    add_para(doc, "• Управление драйвером: Selenium Manager (в составе Selenium 4)")
    add_para(doc, "• Целевой URL: https://ya.ru")
    add_para(doc, "• Каталог автотеста: selenium/")

    add_heading(doc, "4. Установка и порядок выполнения")
    add_para(doc, "Подготовка виртуального окружения и зависимостей:")
    add_code(
        doc,
        """py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r selenium\\requirements.txt""",
    )
    add_para(doc, "Запуск теста КТ 01:")
    add_code(doc, "pytest selenium\\tests\\test_kt01_ya_ru.py -v --browser=chrome")
    add_para(
        doc,
        "Параметр --browser=chrome выбирает браузер через общую фикстуру. "
        "Скриншот сохраняется в файл screenshots/kt01/ya_ru_opened.png.",
    )

    add_heading(doc, "5. Фикстура браузера и assertions")
    add_para(
        doc,
        "Общая фикстура driver создаётся в selenium/conftest.py. Она читает CLI-опцию "
        "--browser, запускает Chrome (по умолчанию), задаёт таймауты загрузки страницы "
        "(30 с), неявного ожидания (5 с) и выполнения скриптов (30 с), после теста "
        "корректно закрывает WebDriver. Фикстура save_screenshot сохраняет PNG "
        "в каталог screenshots/<кт>/.",
    )
    add_para(doc, "Фрагмент фикстуры (сокращённо):")
    add_code(doc, FIXTURE_CODE)
    add_para(
        doc,
        "Тест test_open_ya_ru выполняет переход на https://ya.ru и проверяет: "
        "1) итоговый host относится к семейству ya.ru / yandex (с учётом возможного "
        "редиректа); 2) заголовок страницы непустой; 3) document.readyState равен "
        "complete; 4) скриншот создан и имеет ненулевой размер.",
    )
    add_para(doc, "Фрагмент теста (сокращённо):")
    add_code(doc, TEST_CODE)

    add_heading(doc, "6. Фактический результат выполнения")
    add_para(
        doc,
        "Повторный прогон после добавления pytest.ini (регистрация маркера kt01) "
        "выполнен 2026-10-09. Предупреждений нет. Результат: PASSED.",
    )
    add_para(doc, "Вывод терминала:")
    add_code(doc, TEST_OUTPUT)
    add_para(doc, "Итог: 1 passed за 4.99 с. Exit code: 0.")

    add_heading(doc, "7. Скриншот фактического запуска")
    add_para(
        doc,
        "Ниже приведён подлинный скриншот, сделанный WebDriver после успешной "
        "навигации на https://ya.ru (файл screenshots/kt01/ya_ru_opened.png).",
    )
    doc.add_picture(str(SCREENSHOT), width=Cm(15))
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = caption.add_run("Рисунок 1 — Главная страница ya.ru после запуска WebDriver")
    set_run_font(run, size_pt=11)

    add_heading(doc, "8. Заключение")
    add_para(
        doc,
        "Контрольная точка №1 выполнена: настроены зависимости pytest и Selenium 4, "
        "реализована переиспользуемая фикстура браузера с параметром --browser=chrome, "
        "автотест успешно открывает https://ya.ru и подтверждает корректную навигацию "
        "assertions. Получены воспроизводимые команды запуска, лог PASS и реальный "
        "скриншот. Отчётный файл DOCX сформирован на основании фактического прогона.",
    )
    add_para(
        doc,
        "Ограничения: внешний сайт может менять вёрстку или показывать баннеры; "
        "тест проверяет факт успешной загрузки, а не полный функционал поиска.",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
