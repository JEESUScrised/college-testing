"""Generate reports/KT06.docx from verified Appium KT06 evidence (Russian)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt06"
OUTPUT = Path(__file__).resolve().parent / "KT06.docx"

SCREENSHOTS = [
    ("01_app_home.png", "Рисунок 1 — Главный экран ApiDemos"),
    ("02_app_menu.png", "Рисунок 2 — Меню App"),
    ("03_alert_dialogs.png", "Рисунок 3 — Alert Dialogs"),
    ("04_list_dialog.png", "Рисунок 4 — List dialog"),
    ("05_text_entry_dialog.png", "Рисунок 5 — Text Entry dialog"),
    ("06_back_to_app_menu.png", "Рисунок 6 — Возврат Back на меню App"),
    ("07_back_to_home.png", "Рисунок 7 — Возврат Back на Home"),
    ("08_textfields.png", "Рисунок 8 — Views → TextFields (ввод текста)"),
]

# Final verification suite after scroll fix (7/7)
RESULTS_FINAL = [
    ("TC-06-01", "test_app_starts_and_shows_home", "PASS"),
    ("TC-06-02", "test_navigate_to_app_menu", "PASS"),
    ("TC-06-03", "test_open_alert_dialogs_screen", "PASS"),
    ("TC-06-04", "test_list_dialog_interaction", "PASS"),
    ("TC-06-05", "test_text_entry_dialog_input", "PASS"),
    ("TC-06-06", "test_back_returns_to_previous_screen", "PASS"),
    ("TC-06-07", "test_views_textfields_input", "PASS"),
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
    doc.add_picture(str(path), width=Cm(9))
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
        "КТ №6. Автоматизация мобильного тестирования Android (Appium)",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата: 2026-10-09", center=True)

    add_heading(doc, "1. Цель и объект тестирования")
    add_para(
        doc,
        "Выполнить UI-автотесты официального приложения ApiDemos (Appium sample) "
        "через Appium 3 + UiAutomator2 на Android-эмуляторе. Объект: "
        "package io.appium.android.apis, APK v6.0.18.",
    )

    add_heading(doc, "2. Среда выполнения (новый ПК)")
    add_para(doc, "ОС: Windows 10 (19045), AMD64, AMD Ryzen 5 5600, ~16 ГБ RAM.")
    add_para(doc, "Ускорение эмулятора: AEHD 2.2 (usable).")
    add_para(doc, "Python 3.13.2; pytest 8.4.2; Appium-Python-Client 5.3.1.")
    add_para(doc, "Node.js v22.14.0 / npm 10.9.2; локальный Appium 3.8.0; uiautomator2@8.7.0.")
    add_para(doc, "JAVA_HOME: Android Studio JBR 21 (C:\\Program Files\\Android\\Android Studio\\jbr).")
    add_para(doc, "ANDROID_HOME: C:\\Users\\user\\AppData\\Local\\Android\\Sdk.")
    add_para(doc, "AVD: Medium_Phone_API_36.1 (API 36 / Android 16), udid emulator-5554.")
    add_para(
        doc,
        "APK: ApiDemos-debug.apk v6.0.18, SHA-256 "
        "A9EECF37B26CD084855C530DB81C2BB1B91F4C1B095A04F47AA7C20E2791F686.",
    )
    add_para(
        doc,
        "Примечание: AVD KT06_API33 / system image API 33 не создавались "
        "(вариант B — переиспользование существующего эмулятора).",
    )

    add_heading(doc, "3. Команды запуска")
    add_code(
        doc,
        r""".\scripts\start_kt06_services.ps1 -AvdName Medium_Phone_API_36.1
.\scripts\run_kt06.ps1 -Udid emulator-5554
.\scripts\collect_kt06_artifacts.ps1""",
    )

    add_heading(doc, "4. Хронология прогонов")
    add_para(doc, "Диагностика (один тест): test_app_starts_and_shows_home — PASS за 14.94 с.")
    add_para(
        doc,
        "Прогон №1 (полный suite, до правки scroll): 6 PASS / 1 FAIL за 56.33 с. "
        "FAIL: test_views_textfields_input — TimeoutException на «TextFields» "
        "(пункт вне видимой области списка Views на API 36).",
    )
    add_para(
        doc,
        "Диагностика: UiScrollable.scrollIntoView(description=\"TextFields\") "
        "успешно показывает элемент. В BaseMobilePage добавлен click_menu_item "
        "со прокруткой при необходимости.",
    )
    add_para(doc, "Точечный повтор FAIL-теста после фикса: PASS за 15.13 с.")
    add_para(
        doc,
        "Прогон №2 (полный suite после фикса, без рестарта эмулятора): "
        "7 PASS за 44.63 с, exit 0. Артефакты: "
        "mobile/artifacts/pytest_kt06_20261009_211440.log, "
        "junit_kt06_20261009_211440.xml, report_kt06_20261009_211440.html.",
    )

    add_heading(doc, "5. Результаты финального прогона (7/7)")
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "ID", "Автотест", "Результат"
    for row in RESULTS_FINAL:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")
    add_code(
        doc,
        "============================= 7 passed in 44.63s =============================",
    )

    add_heading(doc, "6. Архитектура")
    add_para(doc, "Page Object: mobile/pages/ (ApiDemosHomePage, AlertDialogsPage, ViewsTextFieldsPage).")
    add_para(doc, "Тесты: mobile/tests/test_kt06_appium.py (7 кейсов, session-scoped driver).")
    add_para(doc, "Между тестами: mobile: startActivity на io.appium.android.apis/.ApiDemos.")

    add_heading(doc, "7. Скриншоты")
    for name, caption in SCREENSHOTS:
        add_shot(doc, name, caption)

    add_heading(doc, "8. Заключение")
    add_para(
        doc,
        "КТ 06 выполнена на новом ПК с существующим эмулятором Medium_Phone_API_36.1. "
        "Диагностический тест и финальный suite (7/7 PASS) подтверждены реальными "
        "артефактами и скриншотами. Первый полный прогон зафиксировал 1 FAIL из-за "
        "необходимости прокрутки списка Views; после исправления Page Object "
        "сценарий TextFields проходит. KT07/KT09 не начинались. Push в GitHub не выполнялся.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №6. Автоматизация мобильного тестирования Android (Appium)",
        "7 PASS",
        "7 passed in 44.63s",
        "Medium_Phone_API_36.1",
        "A9EECF37B26CD084855C530DB81C2BB1B91F4C1B095A04F47AA7C20E2791F686",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    if len(doc.tables) < 1:
        raise AssertionError("Expected results table")
    pictures = list(doc.inline_shapes)
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    if len(pictures) < 8:
        raise AssertionError(f"pictures={len(pictures)}")
    if len(images) < 8:
        raise AssertionError(f"images={len(images)}")
    print(
        f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} "
        f"unique={len(images)} tables={len(doc.tables)}"
    )


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
