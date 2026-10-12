"""Rebuild submission/KT01-KT12_READY_FOR_SUBMISSION.zip with verified evidence."""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(".").resolve()
OUT = ROOT / "submission" / "KT01-KT12_READY_FOR_SUBMISSION.zip"
INCLUDE_ROOTS = ["AGENTS.md", "README.md", "bug-reports", "docs", "reports", "screenshots"]
EXCLUDE_DIR_PARTS = {
    "unusable-visual",
    "_diag",
    "_audit_contact_sheets",
    "__pycache__",
    ".git",
    ".venv",
    "artifacts",
    ".pytest_cache",
    ".mypy_cache",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp"}
EXCLUDE_NAME_SUBSTRINGS = (
    "final_evidence_",
    "jira_blocked",
    "verified_evidence",
    "KT01-KT12_reports.zip",
)


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_PARTS:
        return True
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    name = path.as_posix()
    if any(s in name for s in EXCLUDE_NAME_SUBSTRINGS):
        return True
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


def main() -> None:
    audit_path = ROOT / "docs" / "compliance" / "docx-audit.json"
    if not audit_path.is_file():
        raise SystemExit("Run scripts/final_submission_verify.py before rebuild")

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
