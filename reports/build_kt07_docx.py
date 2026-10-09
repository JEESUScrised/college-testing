"""Generate reports/KT07.docx from verified Selenium Grid evidence (Russian)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt07"
OUTPUT = Path(__file__).resolve().parent / "KT07.docx"

SCREENSHOTS = [
    ("01_remote_session_blank.png", "Рисунок 1 — Remote-сессия через Grid"),
    ("02_navigate_title.png", "Рисунок 2 — Навигация и title"),
    ("03_dom_interaction.png", "Рисунок 3 — Взаимодействие с DOM"),
    ("04_windows_main.png", "Рисунок 4 — Главное окно"),
    ("05_windows_secondary.png", "Рисунок 5 — Вторичное окно"),
    ("06_windows_back_main.png", "Рисунок 6 — Возврат в главное окно"),
    ("07_iframe_host.png", "Рисунок 7 — Host с iframe"),
    ("08_iframe_inside.png", "Рисунок 8 — Внутри iframe"),
    ("09_iframe_default_content.png", "Рисунок 9 — default_content"),
]

RESULTS = [
    ("TC-07-01", "test_remote_session_created", "PASS"),
    ("TC-07-02", "test_navigate_and_title", "PASS"),
    ("TC-07-03", "test_dom_element_interaction", "PASS"),
    ("TC-07-04", "test_window_open_and_switch", "PASS"),
    ("TC-07-05", "test_iframe_interaction_and_context_switch", "PASS"),
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
    add_para(doc, "Группа: ________________________________________", center=True)
    add_para(doc, "")
    add_para(
        doc,
        "КТ №7. Удалённый запуск автотестов через Selenium Grid 4",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке", center=True)
    add_para(doc, "Дата: 2026-10-09", center=True)

    add_heading(doc, "1. Цель и требования")
    add_para(
        doc,
        "Организовать Selenium Grid 4, выполнять браузерные тесты через "
        "RemoteWebDriver и подтвердить работу режимов Standalone и Hub + Node "
        "с реальными сессиями, логами и скриншотами.",
    )

    add_heading(doc, "2. Архитектура Selenium Grid")
    add_para(
        doc,
        "Standalone объединяет Router, Distributor, Session Map, Queue и Node "
        "в одном процессе. Hub + Node разделяет точку входа (Hub) и исполнитель "
        "браузеров (Node). Клиент всегда подключается к http://127.0.0.1:4444.",
    )
    add_para(
        doc,
        "Важно: RemoteWebDriver на localhost — это удалённый протокол Grid, "
        "даже если Hub и браузер на одной машине. Кросс-машинный кластер в этой "
        "работе не разворачивался.",
        bold=True,
    )

    add_heading(doc, "3. Среда")
    add_para(doc, "Windows 10 x64; Java 21 (Android Studio JBR); Python 3.13.2; Selenium 4.50.0.")
    add_para(doc, "Chrome 155.0.8059.39; selenium-server-4.50.0.jar (SeleniumHQ GitHub Releases).")
    add_para(doc, "Grid bind: 127.0.0.1. Node port: 5556 (5555 занят Android emulator/qemu).")
    add_para(
        doc,
        "Event Bus Hub/Node явно на tcp://127.0.0.1:4442 и :4443 — иначе Grid "
        "рекламировал VPN-IP (26.x) и Node не регистрировался.",
    )

    add_heading(doc, "4. Команды запуска")
    add_code(
        doc,
        r""".\selenium\grid\download_server.ps1
.\selenium\grid\start_standalone.ps1
.\selenium\grid\health_check.ps1
.\scripts\run_kt07.ps1
.\selenium\grid\stop_grid.ps1

# Hub + Node (не одновременно со Standalone на :4444)
.\selenium\grid\start_hub_node.ps1
.\selenium\grid\health_check.ps1
.\selenium\grid\stop_grid.ps1""",
    )

    add_heading(doc, "5. Remote WebDriver")
    add_para(
        doc,
        "Фикстура grid_driver создаёт webdriver.Remote(command_executor=grid_url, "
        "options=ChromeOptions()) и не заменяет локальный driver KT01–KT05. "
        "Фикстуры отдаются HTTP-сервером (не file://).",
    )
    add_code(
        doc,
        'options = ChromeOptions()\n'
        'options.set_capability("se:name", "KT07:...")\n'
        'driver = webdriver.Remote("http://127.0.0.1:4444", options=options)\n'
        "# session_id / capabilities сохраняются в selenium/artifacts/kt07/",
    )

    add_heading(doc, "6. Результаты Standalone suite")
    add_para(doc, "Диагностика: 1 PASS. Полный suite: 5 passed in 4.88s, exit 0.")
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "ID", "Автотест", "Результат"
    for row in RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")
    add_code(doc, "============================== 5 passed in 4.88s ==============================")

    add_heading(doc, "7. Hub + Node")
    add_para(
        doc,
        "После остановки Standalone запущены Hub (:4444) и Node (:5556). "
        "Статус: ready=true, nodes=1, uri Node = http://127.0.0.1:5556. "
        "Доказательство сессий: 2 PASS (session + navigate).",
    )

    add_heading(doc, "8. Скриншоты")
    for name, caption in SCREENSHOTS:
        add_shot(doc, name, caption)

    add_heading(doc, "9. Заключение")
    add_para(
        doc,
        "КТ 07 выполнена: официальный Selenium Grid 4, Standalone suite 5/5 PASS, "
        "Hub + Node с регистрацией Node и реальными Remote-сессиями, отчётные "
        "артефакты и скриншоты. Grid слушал только localhost. KT08+ не начинались.",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №7. Удалённый запуск автотестов через Selenium Grid 4",
        "5 passed in 4.88s",
        "Hub + Node",
        "127.0.0.1",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise AssertionError(missing)
    pictures = list(doc.inline_shapes)
    images = [r for r in doc.part.rels.values() if r.reltype == RT.IMAGE]
    if len(pictures) < 9 or len(images) < 9:
        raise AssertionError(f"pictures={len(pictures)} images={len(images)}")
    print(f"VERIFY_OK size={path.stat().st_size} pictures={len(pictures)} unique={len(images)}")


if __name__ == "__main__":
    out = build()
    print(f"Wrote {out}")
    verify(out)
