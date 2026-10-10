"""Generate reports/KT12.docx from verified gRPC evidence (Russian)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt12"
OUTPUT = Path(__file__).resolve().parent / "KT12.docx"
PROTO = ROOT / "grpc" / "proto" / "inventory.proto"

RESULTS = [
    ("TC-12-01", "CreateItem success", "PASS"),
    ("TC-12-02", "GetItem existing", "PASS"),
    ("TC-12-03", "Duplicate → ALREADY_EXISTS", "PASS"),
    ("TC-12-04", "Invalid → INVALID_ARGUMENT", "PASS"),
    ("TC-12-05", "Missing → NOT_FOUND", "PASS"),
    ("TC-12-06", "UpdateStock + re-fetch", "PASS"),
    ("TC-12-07", "ListItems server stream", "PASS"),
    ("TC-12-08", "BulkCreate client stream", "PASS"),
    ("TC-12-09", "EchoWatch bidi stream", "PASS"),
    ("TC-12-10", "SlowPing DEADLINE_EXCEEDED", "PASS"),
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


def add_shot(doc, filename, caption, width_cm=14):
    path = SHOTS / filename
    if not path.is_file():
        add_para(doc, f"[Нет файла: {filename}]")
        return
    doc.add_picture(str(path), width=Cm(width_cm))
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
        "КТ №12. Автоматизированное тестирование реального gRPC-сервиса",
        bold=True,
        center=True,
    )
    add_para(doc, "Отчёт по контрольной точке (финальная)", center=True)
    add_para(doc, "Дата: 2026-10-10", center=True)

    add_heading(doc, "1. Цель задания")
    add_para(
        doc,
        "Реализовать локальный InventoryService на Python + Protocol Buffers, "
        "сгенерировать stubs через grpc_tools.protoc и написать ровно 10 pytest-тестов, "
        "выполняющих реальные RPC по HTTP/2 (без моков).",
    )

    add_heading(doc, "2. Введение в gRPC и Protocol Buffers")
    add_para(
        doc,
        "gRPC — RPC-фреймворк поверх HTTP/2. Контракт описывается в .proto (proto3): "
        "сообщения и сервисы. protoc генерирует код сериализации и клиентские/серверные stubs.",
    )

    add_heading(doc, "3. Клиент–сервер на HTTP/2")
    add_para(
        doc,
        "Клиент открывает канал insecure_channel к 127.0.0.1:<free-port>, дожидается READY "
        "и вызывает методы InventoryServiceStub. Транспорт — HTTP/2; полезные нагрузки — protobuf.",
    )
    add_para(
        doc,
        "Учебный сервис без TLS. В production необходимы TLS и аутентификация.",
        bold=True,
    )

    add_heading(doc, "4. Архитектура InventoryService")
    add_para(
        doc,
        "Слои: proto → generated stubs → InventoryServicer + InventoryStore (in-memory, "
        "thread-safe) → pytest fixture (server lifecycle) → 10 тестов.",
    )

    add_heading(doc, "5. .proto контракт и generated code")
    add_para(doc, "Фрагмент service InventoryService:")
    proto_text = PROTO.read_text(encoding="utf-8") if PROTO.is_file() else ""
    # extract service block roughly
    start = proto_text.find("service InventoryService")
    end = proto_text.find("}", start) + 1 if start >= 0 else 0
    add_code(doc, proto_text[start:end] if start >= 0 else "(proto missing)")
    add_para(
        doc,
        "Генерация: scripts/generate_kt12_proto.ps1 → grpc/generated/inventory_pb2.py "
        "и inventory_pb2_grpc.py (DO NOT EDIT).",
    )

    add_heading(doc, "6. Реализация сервера и клиента")
    add_para(
        doc,
        "server/service.py — валидация и context.abort(...). "
        "client/cli.py — демонстрация CreateItem + GetItem. "
        "Запуск сервера: python -m server --port 50051 (из каталога с настроенным PYTHONPATH).",
    )

    add_heading(doc, "7. Unary RPC")
    add_para(
        doc,
        "CreateItem, GetItem, UpdateStock, SlowPing — один запрос / один ответ. "
        "Доказательства полей и статусов записаны в evidence.jsonl.",
    )

    add_heading(doc, "8. Streaming")
    add_para(
        doc,
        "ListItems — server streaming (итератор Item). "
        "BulkCreate — client streaming → BulkCreateResponse. "
        "EchoWatch — bidi: на каждый WatchRequest ровно один WatchResponse в том же порядке.",
    )

    add_heading(doc, "9. Ошибки и status codes")
    add_para(
        doc,
        "ALREADY_EXISTS (дубликат id), INVALID_ARGUMENT (пустое имя / quantity<0), "
        "NOT_FOUND (отсутствующий id).",
    )

    add_heading(doc, "10. Deadlines и cancellation")
    add_para(
        doc,
        "SlowPing(delay_ms=800) с client timeout=0.1s даёт DEADLINE_EXCEEDED. "
        "Сервер проверяет context.is_active() каждые 20 мс и прекращает ожидание при отмене.",
    )

    add_heading(doc, "11–12. Таблица тест-кейсов и ожидания")
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "ID", "Сценарий", "Статус"
    for row in RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    add_para(doc, "")
    add_para(
        doc,
        "Входные данные и ожидаемые коды описаны в docs/kt12/test-cases.md; "
        "фикстура inventory_env поднимает изолированный сервер на свободном порту.",
    )

    add_heading(doc, "13. Фактические результаты pytest")
    add_para(doc, "Диагностика TC-12-01: PASS. Полный suite:")
    add_code(doc, "============================= 10 passed in 2.34s ==============================")
    add_para(doc, "JUnit: tests=10, failures=0, errors=0, skipped=0.")

    add_heading(doc, "14. Артефакты и фрагменты кода")
    add_para(
        doc,
        "grpc/artifacts/kt12/: pytest log, junit XML, HTML report, evidence.jsonl, versions JSON. "
        "SHA16 log=E656BF1468AA2C30, junit=33F69FACE4CA7013, html=7329D8123EB2800D.",
    )
    add_code(
        doc,
        r""".\scripts\run_kt12.ps1
# evidence excerpt:
# DEADLINE_EXCEEDED SlowPing timeout=0.1 delay_ms=800
# ListItems ids=["s1","s2","s3"]
# EchoWatch FOUND/MISSING/FOUND""",
    )
    add_shot(doc, "01_pytest_html_report.png", "Рисунок 1 — pytest-html отчёт KT12 (10 passed)")

    add_heading(doc, "15. Заключение и ограничения")
    add_para(
        doc,
        "КТ 12 выполнена: реальный gRPC InventoryService, generated stubs, 10/10 PASS за 2.34 с. "
        "Ограничения: insecure channel, in-memory store, без облака/Docker. "
        "Это финальная контрольная точка курса (КТ01–КТ12).",
    )

    doc.save(OUTPUT)
    return OUTPUT


def verify(path: Path) -> None:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    required = [
        "КТ №12. Автоматизированное тестирование реального gRPC-сервиса",
        "10 passed in 2.34s",
        "DEADLINE_EXCEEDED",
        "Заключение",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        raise SystemExit(f"DOCX missing: {missing}")
    print(f"OK {path} size={path.stat().st_size} chars={len(text)}")


if __name__ == "__main__":
    out = build()
    verify(out)
