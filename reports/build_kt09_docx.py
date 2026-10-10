"""Generate reports/KT09.docx from verified Appium gesture evidence (Russian)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt09"
OUTPUT = Path(__file__).resolve().parent / "KT09.docx"

RESULTS = [
    ("TC-09-01", "vertical swipe up (Views)", "PASS"),
    ("TC-09-02", "vertical swipe down (Views)", "PASS"),
    ("TC-09-03", "scroll until TextFields + open", "PASS"),
    ("TC-09-04", "horizontal swipe left (Gallery)", "PASS"),
    ("TC-09-05", "horizontal swipe right (Gallery)", "PASS"),
]

IMAGES = [
    ("01_views_before_swipe_up.png", "Рисунок 1 — Views до swipe up"),
    ("02_views_after_swipe_up.png", "Рисунок 2 — Views после swipe up"),
    ("03_views_before_swipe_down.png", "Рисунок 3 — Views до swipe down"),
    ("04_views_after_swipe_down.png", "Рисунок 4 — Views после swipe down"),
    ("05_before_scroll_to_textfields.png", "Рисунок 5 — До scroll к TextFields"),
    ("06_after_scroll_to_textfields.png", "Рисунок 6 — TextFields виден"),
    ("07_textfields_opened.png", "Рисунок 7 — TextFields открыт"),
    ("08_gallery_before_swipe_left.png", "Рисунок 8 — Gallery до swipe left"),
    ("09_gallery_after_swipe_left.png", "Рисунок 9 — Gallery после swipe left"),
    ("11_gallery_after_swipe_right.png", "Рисунок 10 — Gallery после swipe right"),
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
        "КТ №9. Кроссплатформенное тестирование и жесты (Appium)",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата: 2026-10-10", center=True)

    add_heading(doc, "1. Цель")
    add_para(
        doc,
        "Автоматизировать swipe/scroll на Android через Appium и подтвердить "
        "изменение UI assertions. Структура тестов отделяет намерения от "
        "платформенной реализации; iOS не выполнялся.",
    )
    add_para(
        doc,
        "Презентация cloud.ithub.ru недоступна без авторизации; требования — "
        "из формулировки задания. Соответствие скрытым слайдам не утверждается.",
        bold=True,
    )

    add_heading(doc, "2. Среда Android")
    add_para(doc, "Appium 3.8.0, UiAutomator2 8.7.0, Python 3.13, ApiDemos 6.0.18.")
    add_para(doc, "AVD Medium_Phone_API_36.1 (API 36), udid emulator-5554.")
    add_para(doc, "Переиспользованы сервисы KT06; новый эмулятор/image не создавались.")

    add_heading(doc, "3. Теория жестов")
    add_para(
        doc,
        "Swipe/scroll моделируют жест пальца. В Appium 2+/3 для Android "
        "рекомендуются mobile: swipeGesture и mobile: scrollGesture "
        "(TouchAction устарел). Координаты считаются от размеров окна/элемента "
        "с отступом от системных краёв навигации.",
    )

    add_heading(doc, "4. Реализация")
    add_para(doc, "mobile/gestures/android_gestures.py — AndroidGestures.")
    add_para(doc, "mobile/gestures/platform.py — GesturePort / AndroidGesturePort / IOSGesturePort(заглушка).")
    add_code(
        doc,
        r""".\scripts\start_kt06_services.ps1 -AvdName Medium_Phone_API_36.1
.\scripts\run_kt09.ps1 -Udid emulator-5554""",
    )

    add_heading(doc, "5. Результаты")
    add_para(doc, "Диагностика: PASS. Suite: 5 passed in 54.93s, exit 0.")
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "ID", "Сценарий", "Результат"
    for row in RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")
    add_code(doc, "============================= 5 passed in 54.93s ==============================")

    add_heading(doc, "6. Кроссплатформенность")
    add_para(
        doc,
        "Общий контракт GesturePort позволяет в будущем подключить XCUITest. "
        "Факт: протестирован только Android. iOS NOT RUN — нет симулятора/драйвера/сборки. "
        "Общий код ≠ успешный прогон на двух ОС.",
        bold=True,
    )

    add_heading(doc, "7. Скриншоты")
    for name, caption in IMAGES:
        add_shot(doc, name, caption)

    add_heading(doc, "8. Заключение")
    add_para(
        doc,
        "КТ 09 выполнена на Android: 5 жестовых автотестов PASS, before/after "
        "скриншоты, документация ограничения iOS. KT10 не начиналась.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №9. Кроссплатформенное тестирование и жесты (Appium)",
        "5 passed in 54.93s",
        "iOS",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    pictures = list(doc.inline_shapes)
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    if len(pictures) < 8 or len(images) < 8:
        raise AssertionError(f"pictures={len(pictures)} images={len(images)}")
    if len(doc.tables) < 1:
        raise AssertionError("no table")
    print(f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} unique={len(images)}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
