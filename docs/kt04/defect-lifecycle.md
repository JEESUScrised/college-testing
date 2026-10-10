# KT04 — Defect lifecycle demonstration

## Principle

| Layer | Location | Status |
|---|---|---|
| Historical seeded defective app | `selenium/fixtures/kt04/` | Unchanged; suite MIXED 2 PASS / 3 FAIL |
| Lifecycle fixed copy | `selenium/fixtures/kt04_lifecycle/` | SEED-001/002/003 fixed |
| Retest | `selenium/tests/test_kt04_lifecycle_retest.py` | **3 PASS / 14.40s** (2026-10-10) |
| GitHub Issues | #1–#3 | Preserved Open (historical) |
| Jira Issues | planned QAKT04-* | **BLOCKED** — not created |

## Simulated team roles (honest)

All code fixes and retests in this remediation were performed by the **Cursor coding agent**, not a separate human developer account. When only one Jira account exists, comments must state that clearly — no impersonation.

## Planned Jira transitions (when unblocked)

For each bug: Open → In Progress (assign) → comment with fix summary → Ready for Testing → retest evidence → Done.

## Retest commands

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt04_lifecycle_retest.py -v --browser=chrome
# Historical (expect 3 FAIL):
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt04_defects.py -v --browser=chrome
```
