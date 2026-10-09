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

REGRESSION = """\
KT01–KT03 regression: 11 passed in 53.55s, exit code 0
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
    add_para(doc, "КТ №4. Документирование дефектов и баг-трекинг", bold=True, center=True)
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата выполнения: 2026-10-09", center=True)

    add_heading(doc, "1. Цель работы")
    add_para(
        doc,
        "Цель КТ 04 — продемонстрировать полный цикл работы с дефектами: "
        "выполнение тест-кейсов, обнаружение и воспроизведение ошибок, "
        "оформление баг-репортов и регистрация задач в баг-трекере "
        "(GitHub Issues как аналог Jira).",
    )

    add_heading(doc, "2. Инструменты и среда")
    add_para(doc, "• Windows 11, Python 3.13.9, pytest 8.4.2, Selenium 4.50.0")
    add_para(doc, "• Google Chrome 154.0.8037.98")
    add_para(doc, "• Page Object (LoginPage, RegisterPage, DashboardPage)")
    add_para(doc, "• Баг-трекер: GitHub Issues репозитория JEESUScrised/college-testing")

    add_heading(doc, "3. Тестируемое приложение")
    add_para(
        doc,
        "Campus Portal Demo — локальное учебное HTML/JS-приложение "
        "(вход, регистрация, заказ учебника). В код намеренно внедрены "
        "три seeded-дефекта SEED-001…003. Это не дефекты production-системы.",
    )
    add_para(doc, "Файлы: selenium/fixtures/kt04/*.html, seeded-bugs.md.")

    add_heading(doc, "4. Тест-кейсы")
    add_para(doc, "TC-01 Валидный вход — PASS")
    add_para(doc, "TC-02 Пустой пароль должен отклоняться — FAIL (SEED-001)")
    add_para(doc, "TC-03 Email без TLD должен отклоняться — FAIL (SEED-002)")
    add_para(doc, "TC-04 Количество 0 должно отклоняться — FAIL (SEED-003)")
    add_para(doc, "TC-05 Валидный заказ — PASS")
    add_para(doc, "Подробности: bug-reports/test-cases.md")

    add_heading(doc, "5. Баг-репорты")
    add_para(
        doc,
        "BUG-KT04-001 / Issue #1 — вход с пустым паролем (Major/High, Open).",
    )
    add_para(
        doc,
        "BUG-KT04-002 / Issue #2 — email user@mail принимается (Major/High, Open).",
    )
    add_para(
        doc,
        "BUG-KT04-003 / Issue #3 — заказ с qty=0 (Minor/Medium, Open).",
    )
    add_para(doc, "Полные карточки: bug-reports/bug-reports.md")

    add_heading(doc, "6. Баг-трекер (GitHub Issues)")
    add_para(doc, "Созданы реальные issues (не черновики):")
    add_para(doc, "https://github.com/JEESUScrised/college-testing/issues/1")
    add_para(doc, "https://github.com/JEESUScrised/college-testing/issues/2")
    add_para(doc, "https://github.com/JEESUScrised/college-testing/issues/3")
    add_para(doc, "Метки: bug, kt04, educational, severity:*, priority:*.")

    add_heading(doc, "7. Фактические результаты прогона")
    add_code(doc, KT04_OUTPUT)
    add_code(doc, REGRESSION)
    add_para(
        doc,
        "FAIL по TC-02/03/04 ожидаемы: автотесты проверяют корректное поведение "
        "продукта и тем самым подтверждают наличие seeded-дефектов.",
    )

    add_heading(doc, "8. Скриншоты")
    for name, caption in SCREENSHOTS:
        add_shot(doc, name, caption)

    add_heading(doc, "9. Жизненный цикл дефекта")
    add_para(doc, "Open → In Progress → Resolved → Closed.")
    add_para(
        doc,
        "Все три дефекта оставлены в статусе Open: исправления и ретесты "
        "не выполнялись в рамках КТ 04.",
    )

    add_heading(doc, "10. Заключение")
    add_para(
        doc,
        "КТ 04 выполнена: подготовлено учебное приложение с тремя seeded-багами, "
        "описаны и прогнаны 5 тест-кейсов (2 PASS / 3 FAIL), оформлены баг-репорты, "
        "созданы GitHub Issues #1–#3, собраны подлинные скриншоты и отчёт DOCX. "
        "Регрессия КТ 01–03 прошла успешно (11 passed).",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №4. Документирование дефектов и баг-трекинг",
        "3 failed, 2 passed in 18.08s",
        "issues/1",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    pictures = list(doc.inline_shapes)
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    if len(pictures) < len(SCREENSHOTS):
        raise AssertionError(f"pictures={len(pictures)}")
    if not images:
        raise AssertionError("no images")
    print(f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} unique={len(images)}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
