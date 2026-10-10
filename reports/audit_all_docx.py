"""Audit KT01–KT12 DOCX presence, openability, titles, images, placeholders."""

from __future__ import annotations

import json
from pathlib import Path

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from report_title import missing_personal_fields

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs" / "compliance" / "docx-audit.json"


def audit_one(path: Path) -> dict:
    info: dict = {
        "file": path.name,
        "exists": path.is_file(),
        "size": path.stat().st_size if path.is_file() else 0,
        "openable": False,
        "paragraphs": 0,
        "tables": 0,
        "pictures": 0,
        "unique_images": 0,
        "title_guess": "",
        "has_conclusion": False,
        "placeholder_fields": False,
        "missing_image_markers": 0,
        "issues": [],
    }
    if not path.is_file():
        info["issues"].append("MISSING_FILE")
        return info
    try:
        doc = Document(str(path))
    except Exception as exc:  # noqa: BLE001
        info["issues"].append(f"OPEN_FAIL:{exc}")
        return info
    info["openable"] = True
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    info["paragraphs"] = len(paras)
    info["tables"] = len(doc.tables)
    info["pictures"] = len(list(doc.inline_shapes))
    info["unique_images"] = len([r for r in doc.part.rels.values() if r.reltype == RT.IMAGE])
    # title: first bold-ish or first non-discipline heading-like line
    for t in paras[:12]:
        if t.startswith("КТ") or "КТ №" in t or t.startswith("KT"):
            info["title_guess"] = t[:120]
            break
    if not info["title_guess"] and paras:
        info["title_guess"] = paras[min(5, len(paras) - 1)][:120]
    joined = "\n".join(paras)
    info["has_conclusion"] = "Заключение" in joined or "заключение" in joined
    info["placeholder_fields"] = "____" in joined or "Студент:" in joined
    info["missing_image_markers"] = joined.count("Скриншот отсутствует") + joined.count("Нет файла:")
    if info["pictures"] == 0 and "KT12" not in path.name:
        # KT12 may be lighter on screenshots
        pass
    if not info["has_conclusion"]:
        info["issues"].append("NO_CONCLUSION")
    if info["missing_image_markers"]:
        info["issues"].append("MISSING_IMAGE_PLACEHOLDERS")
    if info["paragraphs"] < 8:
        info["issues"].append("TOO_SHORT")
    return info


def main() -> None:
    rows = [audit_one(ROOT / f"KT{i:02d}.docx") for i in range(1, 13)]
    summary = {
        "date": "2026-10-11",
        "all_present": all(r["exists"] and r["openable"] for r in rows),
        "missing_personal_metadata": missing_personal_fields(),
        "reports": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"all_present={summary['all_present']}")
    for r in rows:
        print(
            f"{r['file']}: open={r['openable']} pics={r['pictures']} "
            f"tables={r['tables']} issues={r['issues'] or '-'}"
        )


if __name__ == "__main__":
    main()
