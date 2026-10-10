"""Generate reports/KT04.docx from verified KT04 artifacts."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt04"
OUTPUT = Path(__file__).resolve().parent / "KT04.docx"

SCREENSHOTS = [
    ("tc01_valid_login.png", "Рисунок 1 — TC-01 PASS: валидный вход"),
    ("tc02_seed001_empty_password.png", "Рисунок 2 — SEED-001: вход с пустым паролем открыл кабинет"),
    ("tc03_seed002_invalid_email.png", "Рисунок 3 — SEED-002: регистрация с email user@mail успешна"),
    ("tc04_seed003_zero_quantity.png", "Рисунок 4 — SEED-003: заказ с количеством 0 принят"),
    ("tc05_valid_order.png", "Рисунок 5 — TC-05 PASS: валидный заказ"),
]

LIFECYCLE = SHOTS / "lifecycle"
LIFE_SHOTS = [
    (LIFECYCLE / "retest_seed001_empty_password.png", "Рисунок 6 — Lifecycle retest SEED-001 REJECTED (PASS)"),
    (LIFECYCLE / "retest_seed002_invalid_email.png", "Рисунок 7 — Lifecycle retest SEED-002 REJECTED (PASS)"),
    (LIFECYCLE / "retest_seed003_zero_quantity.png", "Рисунок 8 — Lifecycle retest SEED-003 REJECTED (PASS)"),
]

KT04_OUTPUT = """\
collected 5 items
test_tc01_valid_login_passes PASSED
test_tc02_empty_password_should_be_rejected FAILED
test_tc03_invalid_email_should_be_rejected FAILED
test_tc04_zero_quantity_should_be_rejected FAILED
test_tc05_valid_order_passes PASSED
======================== 3 failed, 2 passed in 18.08s =========================
exit code: 1
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


def add_shot(doc: Document, path: Path, caption: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    doc.add_picture(str(path), width=Cm(14))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(caption)
    set_run_font(run, size_pt=11)


def build() -> Path:
    missing = [n for n, _ in SCREENSHOTS if not (SHOTS / n).is_file()]
    if missing:
        raise FileNotFoundError(missing)

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

    add_heading(doc, "1. Цель работы (по заданию преподавателя)")
    add_para(
        doc,
        "Ознакомиться с возможностями Jira; создать проект; настроить типы/приоритеты/"
        "workflow/компоненты; оформить баг-репорты; назначить задачи; провести дефекты "
        "по стадиям; исправить и перепроверить; закрыть; показать статистику и отчёты Jira.",
    )

    add_heading(doc, "2. Обзор Jira и фактический статус доступа")
    add_para(
        doc,
        "Jira — система учёта задач/дефектов с workflow, назначениями, комментариями "
        "и отчётностью. В этой сессии реального workspace нет: открыта страница "
        "входа Atlassian (id.atlassian.com/login), MCP/API credentials отсутствуют. "
        "Проект QAKT04 и issue keys НЕ создавались (не выдуманы).",
        bold=True,
    )

    add_heading(doc, "3. Планируемая конфигурация проекта QAKT04")
    add_para(doc, "Name: College QA Defect Lifecycle; Key: QAKT04; Kanban/Software если доступно.")
    add_para(doc, "Issue types: Bug, Task, Improvement. Components: Authentication, Registration, Order Processing.")
    add_para(doc, "Workflow (план): Open → In Progress → Ready for Testing → Done.")
    add_para(doc, "Факт: конфигурация не применена — docs/kt04/jira-project.md.")

    add_heading(doc, "4. Инструменты и среда")
    add_para(doc, "Windows; Python 3.13; pytest 8.4.2; Selenium 4.50; Chrome.")
    add_para(doc, "Page Object: LoginPage, RegisterPage, DashboardPage.")
    add_para(doc, "Исторический трекер: GitHub Issues #1–#3. Jira: BLOCKED.")

    add_heading(doc, "5. Учебное приложение Campus Portal Demo")
    add_para(
        doc,
        "Локальное HTML/JS приложение (вход, регистрация, заказ). "
        "Три намеренных seeded-дефекта в selenium/fixtures/kt04/. "
        "Отдельная исправленная копия: selenium/fixtures/kt04_lifecycle/.",
    )

    add_heading(doc, "6. Исторические тест-кейсы (seeded)")
    add_para(doc, "TC-01 Валидный вход — PASS")
    add_para(doc, "TC-02 Пустой пароль должен отклоняться — FAIL (SEED-001)")
    add_para(doc, "TC-03 Email без TLD должен отклоняться — FAIL (SEED-002)")
    add_para(doc, "TC-04 Количество 0 должно отклоняться — FAIL (SEED-003)")
    add_para(doc, "TC-05 Валидный заказ — PASS")
    add_code(doc, KT04_OUTPUT)

    add_heading(doc, "7. Три дефекта и баг-репорты")
    add_para(doc, "BUG-KT04-001 / GitHub #1 — пустой пароль (Major/High). Jira key: не создан.")
    add_para(doc, "BUG-KT04-002 / GitHub #2 — email user@mail (Major/High). Jira key: не создан.")
    add_para(doc, "BUG-KT04-003 / GitHub #3 — qty=0 (Minor/Medium). Jira key: не создан.")
    add_para(doc, "Карточки: bug-reports/bug-reports.md; registry: docs/kt04/jira-issues.md.")

    add_heading(doc, "8. GitHub Issues (сохранены)")
    add_para(doc, "https://github.com/JEESUScrised/college-testing/issues/1")
    add_para(doc, "https://github.com/JEESUScrised/college-testing/issues/2")
    add_para(doc, "https://github.com/JEESUScrised/college-testing/issues/3")

    add_heading(doc, "9. Скриншоты — исторический seeded suite")
    for name, caption in SCREENSHOTS:
        add_shot(doc, SHOTS / name, caption)

    add_heading(doc, "10. Lifecycle: исправленная копия и before/after")
    add_para(
        doc,
        "fixtures/kt04 не изменялись. В kt04_lifecycle: reject empty password; "
        "email с TLD; reject qty<=0. Исправления выполнены Cursor-агентом "
        "(образовательная симуляция ролей; без impersonation).",
    )
    add_para(doc, "Retest 2026-10-10: 3 passed in 14.40s. Retest 2026-10-11: 3 passed in 8.74s.")
    add_code(
        doc,
        "============================== 3 passed in 8.74s ==============================\n"
        "test_lifecycle_empty_password_rejected PASSED\n"
        "test_lifecycle_invalid_email_rejected PASSED\n"
        "test_lifecycle_zero_quantity_rejected PASSED",
    )
    for path, caption in LIFE_SHOTS:
        add_shot(doc, path, caption)

    add_heading(doc, "11. Jira assignments / comments / transitions")
    add_para(
        doc,
        "Фактические назначения, комментарии и переходы в Jira: отсутствуют (BLOCKED). "
        "План: docs/kt04/defect-lifecycle.md.",
        bold=True,
    )

    add_heading(doc, "12. Нативные отчёты Jira")
    add_para(
        doc,
        "Native filters/dashboards/statistics недоступны без проекта. "
        "Локальные таблицы не выдаются за отчёты Jira. См. docs/kt04/jira-reporting.md.",
    )

    add_heading(doc, "13. Матрица соответствия требованиям")
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Требование", "Статус", "Доказательство"
    for row in [
        ("Ознакомление с Jira", "PARTIAL", "Описание; UI login открыт"),
        ("Создание проекта", "BLOCKED", "jira-project.md"),
        ("Типы/приоритеты/компоненты/workflow", "BLOCKED", "план, не применено"),
        ("Детальные баг-репорты", "PASS (local+GitHub)", "bug-reports.md"),
        ("Назначения / комментарии Jira", "BLOCKED", "—"),
        ("Переходы workflow", "BLOCKED", "—"),
        ("Исправление дефектов", "PASS (lifecycle copy)", "kt04_lifecycle/"),
        ("Retest", "PASS", "3/3 в 8.74s"),
        ("Закрытие в Jira", "BLOCKED", "—"),
        ("Статистика / native reports", "BLOCKED", "jira-reporting.md"),
    ]:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")

    add_heading(doc, "14. Заключение")
    add_para(
        doc,
        "КТ 04 частично выполнена: seeded 2 PASS/3 FAIL, GitHub #1–#3, lifecycle fixes + "
        "Selenium retest 3/3 PASS. Полный цикл в реальном Jira — BLOCKED до входа "
        "пользователя в Atlassian и явного разрешения создать QAKT04 и issues. "
        "КТ 04 не отмечается как 100% complete.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "работа с баг-трекером Jira",
        "3 failed, 2 passed in 18.08s",
        "3 passed in 8.74s",
        "BLOCKED",
        "issues/1",
        "Матрица соответствия",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    pictures = list(doc.inline_shapes)
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    expected = len(SCREENSHOTS) + len(LIFE_SHOTS)
    if len(pictures) < expected:
        raise AssertionError(f"pictures={len(pictures)} expected>={expected}")
    if not images:
        raise AssertionError("no images")
    if len(doc.tables) < 1:
        raise AssertionError("expected compliance table")
    print(f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} unique={len(images)}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
