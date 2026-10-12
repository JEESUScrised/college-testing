"""Rebuild submission/KT01-KT12_READY_FOR_SUBMISSION.zip with verified evidence."""
from __future__ import annotations

import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from docx import Document

ROOT = Path(".").resolve()
OUT = ROOT / "submission" / "KT01-KT12_READY_FOR_SUBMISSION.zip"
INCLUDE_ROOTS = ["AGENTS.md", "README.md", "bug-reports", "docs", "reports", "screenshots"]
EXCLUDE_DIR_PARTS = {
    "unusable-visual",
    "_diag",
    "_audit_contact_sheets",
    "__pycache__",
    ".git",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_PARTS:
        return True
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    # Do not ship Python builders inside reports zip payload? Keep them — prior zip had reports/*.py
    return False


def collect_files() -> list[Path]:
    files: list[Path] = []
    for name in INCLUDE_ROOTS:
        p = ROOT / name
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and not should_skip(f.relative_to(ROOT)):
                    files.append(f)
    return files


def audit_docx() -> dict:
    reports = sorted((ROOT / "reports").glob("KT*.docx"))
    items = []
    for docx_path in reports:
        doc = Document(str(docx_path))
        pics = 0
        for rel in doc.part.rels.values():
            if "image" in rel.reltype:
                pics += 1
        text = "\n".join(p.text for p in doc.paragraphs[:30])
        items.append(
            {
                "file": docx_path.name,
                "size": docx_path.stat().st_size,
                "pictures": pics,
                "has_student": "Прилепов" in text or "прилепов" in text.lower(),
                "opens": True,
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reports": items,
        "note": "Screenshot remediation 2026-10-12; KT09 excluded from visual rewrite.",
    }


def main() -> None:
    audit = audit_docx()
    audit_path = ROOT / "docs" / "compliance" / "docx-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", audit_path)

    files = collect_files()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            arc = f.relative_to(ROOT).as_posix()
            zf.write(f, arc)
    print("wrote", OUT, "files=", len(files), "bytes=", OUT.stat().st_size)

    with zipfile.ZipFile(OUT) as zf:
        names = zf.namelist()
        assert "reports/KT02.docx" in names
        assert "reports/KT09.docx" in names
        assert not any("unusable-visual" in n for n in names)
        assert "docs/compliance/SCREENSHOT_VISUAL_AUDIT.md" in names
        print("zip_verify_ok entries=", len(names))


if __name__ == "__main__":
    main()
