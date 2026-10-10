"""Generate reports/KT04.docx from verified KT04 + real Jira evidence."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt04"
JIRA = SHOTS / "jira"
OUTPUT = Path(__file__).resolve().parent / "KT04.docx"

SCREENSHOTS = [
    ("tc01_valid_login.png", "Рисунок 1 — TC-01 PASS: валидный вход"),
    ("tc02_seed001_empty_password.png", "Рисунок 2 — SEED-001: пустой пароль принят"),
    ("tc03_seed002_invalid_email.png", "Рисунок 3 — SEED-002: email user@mail принят"),
    ("tc04_seed003_zero_quantity.png", "Рисунок 4 — SEED-003: qty=0 принят"),
    ("tc05_valid_order.png", "Рисунок 5 — TC-05 PASS: валидный заказ"),
]

LIFECYCLE = SHOTS / "lifecycle"
LIFE_SHOTS = [
    (LIFECYCLE / "retest_seed001_empty_password.png", "Рисунок 6 — Lifecycle retest SEED-001 PASS"),
    (LIFECYCLE / "retest_seed002_invalid_email.png", "Рисунок 7 — Lifecycle retest SEED-002 PASS"),
    (LIFECYCLE / "retest_seed003_zero_quantity.png", "Рисунок 8 — Lifecycle retest SEED-003 PASS"),
]

JIRA_SHOTS = [
    (JIRA / "01_board_college_qa.png", "Рисунок 9 — Jira board College QA Defect Lifecycle (KAN)"),
    (JIRA / "02_issue_KAN-4.png", "Рисунок 10 — Jira KAN-4 Done + comments"),
    (JIRA / "03_filter_bugs_done.png", "Рисунок 11 — Jira filter: 3 Bugs Done"),
]

KT04_OUTPUT = """\
======================== 3 failed, 2 passed in 18.08s =========================
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


def add_shot(doc: Document, path: Path, caption: str) -> None:
    if not path.is_file():
        add_para(doc, f"[Скриншот отсутствует: {path.name}]")
        return
    doc.add_picture(str(path), width=Cm(14))
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
        "КТ №4. Составление отчетов о дефектах и работа с баг-трекером Jira",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата обновления: 2026-10-11", center=True)

    add_heading(doc, "1. Цель работы")
    add_para(
        doc,
        "Ознакомиться с Jira; создать проект; настроить типы/приоритеты/workflow; "
        "оформить баг-репорты; назначить; провести по стадиям; исправить; ретест; закрыть; "
        "показать статистику и отчёты Jira.",
    )

    add_heading(doc, "2. Реальный проект Jira")
    add_para(doc, "Site: https://collegeqakt04.atlassian.net")
    add_para(doc, "Project: College QA Defect Lifecycle, key KAN (planned QAKT04 — auto key KAN).")
    add_para(doc, "Board: https://collegeqakt04.atlassian.net/jira/software/projects/KAN/boards/2")
    add_para(doc, "Issue types: Epic, Story, Task, Баг, Subtask (Bug добавлен вручную).")
    add_para(doc, "Workflow: Open → In Progress → Ready for Testing → Done.")
    add_para(doc, "Components: labels authentication / registration / order-processing.")

    add_heading(doc, "3. Три реальных Jira Bug")
    add_para(doc, "KAN-4 — Login accepts empty password — High — Done — assignee JEESUS")
    add_para(doc, "https://collegeqakt04.atlassian.net/browse/KAN-4")
    add_para(doc, "KAN-5 — Registration accepts email without TLD — High — Done")
    add_para(doc, "https://collegeqakt04.atlassian.net/browse/KAN-5")
    add_para(doc, "KAN-6 — Order accepts quantity zero — Medium — Done")
    add_para(doc, "https://collegeqakt04.atlassian.net/browse/KAN-6")
    add_para(doc, "GitHub #1–#3 сохранены как исторические записи.")

    add_heading(doc, "4. Исторический seeded suite (не переписывался)")
    add_para(doc, "Campus Portal fixtures/kt04: 2 PASS / 3 FAIL (ожидаемые учебные FAIL).")
    add_code(doc, KT04_OUTPUT)

    add_heading(doc, "5. Скриншоты seeded suite")
    for name, caption in SCREENSHOTS:
        add_shot(doc, SHOTS / name, caption)

    add_heading(doc, "6. Lifecycle copy + Selenium retest")
    add_para(doc, "fixtures/kt04_lifecycle: empty password / email TLD / qty>0. Retest 3 passed in 8.74s.")
    add_code(
        doc,
        "============================== 3 passed in 8.74s ==============================",
    )
    for path, caption in LIFE_SHOTS:
        add_shot(doc, path, caption)

    add_heading(doc, "7. Jira assignments, comments, transitions")
    add_para(
        doc,
        "На каждом баге: assign JEESUS; 3 комментария (triage / fix / retest); "
        "переходы Open→In Progress→Ready for Testing→Done. "
        "Все роли выполнялись на одном аккаунте JEESUS Cursor-агентом (образовательная симуляция, без impersonation).",
    )

    add_heading(doc, "8. Скриншоты Jira")
    for path, caption in JIRA_SHOTS:
        add_shot(doc, path, caption)

    add_heading(doc, "9. Отчёты / статистика Jira")
    add_para(doc, "Filter Type=Баг: 3 issues, все Done. High=2, Medium=1.")
    add_para(doc, "Native issue navigator + board; см. docs/kt04/jira-reporting.md.")

    add_heading(doc, "10. Матрица соответствия")
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Требование", "Статус", "Доказательство"
    for row in [
        ("Ознакомление с Jira", "PASS", "Реальный сайт collegeqakt04"),
        ("Создание проекта", "PASS", "KAN College QA Defect Lifecycle"),
        ("Типы/приоритеты/workflow", "PASS", "Баг + Ready for Testing"),
        ("Детальные баг-репорты", "PASS", "KAN-4/5/6 + bug-reports.md"),
        ("Назначения / комментарии", "PASS", "JEESUS + 3 comments/issue"),
        ("Переходы workflow", "PASS", "→ Done"),
        ("Исправление + retest", "PASS", "kt04_lifecycle 3/3"),
        ("Закрытие в Jira", "PASS", "Готово"),
        ("Статистика / filters", "PASS", "filter 3 Bugs Done"),
    ]:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")

    add_heading(doc, "11. Заключение")
    add_para(
        doc,
        "КТ 04: реальный Jira проект KAN с тремя Bugs (KAN-4/5/6), полный lifecycle до Done, "
        "локальные lifecycle-фиксы и Selenium retest 3/3 PASS. "
        "Исторический seeded 2/3 FAIL и GitHub #1–#3 сохранены. "
        "Ограничения: ключ KAN вместо QAKT04; components = labels.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "работа с баг-трекером Jira",
        "collegeqakt04.atlassian.net",
        "KAN-4",
        "KAN-5",
        "KAN-6",
        "3 passed in 8.74s",
        "3 failed, 2 passed",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    pictures = list(doc.inline_shapes)
    if len(pictures) < 10:
        raise AssertionError(f"pictures={len(pictures)}")
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    if not images:
        raise AssertionError("no images")
    print(f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} unique={len(images)}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
