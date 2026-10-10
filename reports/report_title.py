"""Shared title-page metadata for KT DOCX generators."""

from __future__ import annotations

import json
from pathlib import Path

from docx.oxml.ns import qn
from docx.shared import Pt

META_PATH = Path(__file__).resolve().parent / "report_metadata.json"


def load_metadata() -> dict:
    if META_PATH.is_file():
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    return {
        "discipline": "Модульное тестирование веб-приложений",
        "student": "",
        "group": "",
    }


def _field(label: str, value: str) -> str:
    value = (value or "").strip()
    if value:
        return f"{label}: {value}"
    width = max(8, 40 - len(label))
    return f"{label}: " + ("_" * width)


def set_run_font(run, size_pt: float = 12, bold: bool = False, name: str = "Times New Roman") -> None:
    run.bold = bold
    run.font.size = Pt(size_pt)
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def add_title_fields(doc, add_para) -> None:
    """add_para(doc, text, *, bold=False, center=False) callback from each builder."""
    meta = load_metadata()
    add_para(
        doc,
        f"Дисциплина: {meta.get('discipline') or 'Модульное тестирование веб-приложений'}",
        center=True,
    )
    institution = (meta.get("institution") or "").strip()
    if institution:
        add_para(doc, f"Учебное заведение: {institution}", center=True)
    add_para(doc, _field("Студент", meta.get("student", "")), center=True)
    add_para(doc, _field("Группа", meta.get("group", "")), center=True)


def missing_personal_fields() -> list[str]:
    meta = load_metadata()
    return [k for k in ("student", "group") if not (meta.get(k) or "").strip()]
