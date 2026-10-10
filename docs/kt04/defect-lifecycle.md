# KT04 — Defect lifecycle demonstration

## Principle

| Layer | Location | Status |
|---|---|---|
| Historical seeded defective app | `selenium/fixtures/kt04/` | Unchanged; suite MIXED **2 PASS / 3 FAIL** |
| Lifecycle fixed copy | `selenium/fixtures/kt04_lifecycle/` | SEED-001/002/003 fixed |
| Retest (2026-10-10) | `test_kt04_lifecycle_retest.py` | **3 PASS / 14.40s** |
| Retest (2026-10-11) | same | **3 PASS / 8.74s** |
| GitHub Issues | #1–#3 | Preserved Open (historical) |
| Jira Issues / transitions | QAKT04 | **BLOCKED** — not created |

## Fixes in lifecycle copy (actual code)

| SEED | File | Fix |
|---|---|---|
| 001 | `kt04_lifecycle/index.html` | Reject empty password before dashboard redirect |
| 002 | `kt04_lifecycle/register.html` | Email must match `local@domain.tld` |
| 003 | `kt04_lifecycle/dashboard.html` | Reject `qty <= 0` |

Original `selenium/fixtures/kt04/` **not modified**.

## Before / after evidence

| Defect | BEFORE (seeded) | AFTER (lifecycle) |
|---|---|---|
| Empty password | TC-02 FAIL; `tc02_seed001_empty_password.png` | retest PASS; `lifecycle/retest_seed001_empty_password.png` |
| Invalid email | TC-03 FAIL; `tc03_seed002_invalid_email.png` | retest PASS; `lifecycle/retest_seed002_invalid_email.png` |
| Qty=0 | TC-04 FAIL; `tc04_seed003_zero_quantity.png` | retest PASS; `lifecycle/retest_seed003_zero_quantity.png` |

## Simulated team roles (honest)

All code fixes and Selenium retests were performed by the **Cursor coding agent**.  
No separate human developer/QA accounts were used. When Jira is available with one account, comments must state the educational simulated-role workflow — **no impersonation**.

## Planned Jira transitions (when unblocked + approved)

For each bug: Open → In Progress → comment (fix) → Ready for Testing → comment (retest) → Done.

Actual transition timestamps/keys: **N/A until Jira exists**.

## Commands

```powershell
# Historical (expect 3 FAIL / 2 PASS):
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt04_defects.py -v --browser=chrome

# Lifecycle retest (expect 3 PASS):
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt04_lifecycle_retest.py -v --browser=chrome
```

Latest lifecycle artifacts: `selenium/artifacts/kt04/junit_lifecycle_20261011.xml`.
