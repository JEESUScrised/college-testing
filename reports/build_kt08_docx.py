"""Generate reports/KT08.docx from verified visual regression evidence (Russian)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt08"
BASELINES = ROOT / "selenium" / "baselines" / "kt08"
ARTIFACTS = ROOT / "selenium" / "artifacts" / "kt08"
OUTPUT = Path(__file__).resolve().parent / "KT08.docx"

RESULTS = [
    ("TC-08-01", "match baseline", "0.0000%", "0", "PASS"),
    ("TC-08-02", "text/color change", "1.1082%", "13021", "PASS"),
    ("TC-08-03", "layout shift", "5.0647%", "59511", "PASS"),
    ("TC-08-04", "significant diff", "99.8457%", "1173203", "PASS"),
    ("TC-08-05", "dimension mismatch", "n/a", "—", "PASS"),
]

IMAGES = [
    (BASELINES / "home_baseline.png", "Рисунок 1 — Approved baseline (home_baseline.png)"),
    (SHOTS / "01_home_actual.png", "Рисунок 2 — Actual match screenshot"),
    (SHOTS / "02_text_color_actual.png", "Рисунок 3 — Text/color change actual"),
    (ARTIFACTS / "02_text_color_overlay.png", "Рисунок 4 — Overlay text/color diffs"),
    (SHOTS / "03_layout_shift_actual.png", "Рисунок 5 — Layout shift actual"),
    (ARTIFACTS / "03_layout_shift_overlay.png", "Рисунок 6 — Overlay layout shift"),
    (SHOTS / "04_significant_actual.png", "Рисунок 7 — Significant change actual"),
    (ARTIFACTS / "04_significant_overlay.png", "Рисунок 8 — Overlay significant diffs"),
    (SHOTS / "05_dimension_mismatch_actual.png", "Рисунок 9 — Smaller viewport (dimension mismatch)"),
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


def add_code(doc: Document, code: str) -> None:
    for line in code.strip("\n").splitlines():
        p = doc.add_paragraph()
        run = p.add_run(line if line else " ")
        set_run_font(run, size_pt=9, name="Consolas")
        p.paragraph_format.space_after = Pt(0)


def add_shot(doc: Document, path: Path, caption: str) -> None:
    if not path.is_file():
        add_para(doc, f"[Нет файла: {path}]")
        return
    doc.add_picture(str(path), width=Cm(12))
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
    add_para(doc, "")
    add_para(
        doc,
        "КТ №8. Скриншотное тестирование (Selenium + Pillow)",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата: 2026-10-09", center=True)

    add_heading(doc, "1. Цель")
    add_para(
        doc,
        "Реализовать visual regression: захват реальных скриншотов браузера "
        "Selenium и сравнение с утверждёнными baseline через Pillow с "
        "диагностическими diff-артефактами.",
    )
    add_para(
        doc,
        "Презентация cloud.ithub.ru (КТ08) без авторизации недоступна; "
        "требования взяты из формулировки задания. Полное соответствие скрытым "
        "слайдам не утверждается.",
        bold=True,
    )

    add_heading(doc, "2. Теория visual regression")
    add_para(
        doc,
        "Скриншотное сравнение выявляет нежелательные визуальные изменения UI "
        "(цвет, текст, сдвиг блоков, пропавшие элементы), которые могут "
        "пропустить селекторные тесты. Эталон (baseline) утверждается вручную; "
        "каждый прогон сравнивает новый снимок с эталоном попиксельно с допуском "
        "цвета и порогом доли изменённых пикселей.",
    )

    add_heading(doc, "3. Реализация")
    add_para(doc, "Selenium 4 Chrome фиксирует окно 1400×1000 и сохраняет PNG.")
    add_para(
        doc,
        "Pillow (`selenium/visual/compare.py`): RGB-загрузка, запрет auto-resize, "
        "допуск color_tolerance=12, threshold match=0.75%, mask и красный overlay. "
        "Baseline при FAIL не перезаписывается.",
    )
    add_code(
        doc,
        r""".\.venv\Scripts\python.exe selenium\visual\generate_kt08_baselines.py
.\scripts\run_kt08.ps1""",
    )

    add_heading(doc, "4. Baseline")
    add_para(
        doc,
        "Файл selenium/baselines/kt08/home_baseline.png получен реальным Chrome "
        "из home.html; размер изображения 1384×849; манифест baseline_manifest.json.",
    )

    add_heading(doc, "5. Результаты прогона")
    add_para(doc, "Диагностика: TC-08-01 PASS. Suite: 5 passed in 13.71s, exit 0.")
    table = doc.add_table(rows=1, cols=5)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text, hdr[4].text = (
        "ID",
        "Сценарий",
        "Diff%",
        "Changed px",
        "Статус",
    )
    for row in RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")
    add_code(doc, "============================= 5 passed in 13.71s ==============================")

    add_heading(doc, "6. Метрики")
    add_para(
        doc,
        "changed_pixels — число пикселей, где max(|ΔR|,|ΔG|,|ΔB|) > tolerance. "
        "diff_percent = changed_pixels / (width*height) * 100. "
        "DIMENSION_MISMATCH фиксируется отдельно без масштабирования "
        "(пример: 1384×849 vs 884×549).",
    )

    add_heading(doc, "7. Скриншоты и diff")
    for path, caption in IMAGES:
        add_shot(doc, path, caption)

    add_heading(doc, "8. Плюсы и ограничения")
    add_para(doc, "Плюсы: ловит визуальные дефекты; понятные overlay; детерминированные локальные фикстуры.")
    add_para(
        doc,
        "Ограничения: чувствительность к DPI/шрифтам/версии Chrome; не заменяет "
        "функциональные проверки; шумные страницы требуют осторожного порога.",
    )

    add_heading(doc, "9. Заключение")
    add_para(
        doc,
        "КТ 08 выполнена: Pillow-утилита, approved baseline, 5 автотестов "
        "(match / text-color / layout / significant / dimensions), suite 5/5 PASS, "
        "артефакты и отчёт. KT09+ не начинались.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №8. Скриншотное тестирование (Selenium + Pillow)",
        "5 passed in 13.71s",
        "DIMENSION_MISMATCH",
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
