# KT04 — Defect lifecycle (local + REAL Jira)

## Layers

| Layer | Location | Status |
|---|---|---|
| Historical seeded app | `selenium/fixtures/kt04/` | Unchanged; **2 PASS / 3 FAIL** |
| Lifecycle fixed copy | `selenium/fixtures/kt04_lifecycle/` | SEED-001/002/003 fixed |
| Selenium retest | `test_kt04_lifecycle_retest.py` | **3 PASS / 8.74s** (2026-10-11) |
| GitHub Issues | #1–#3 | Preserved Open (historical) |
| Jira Issues | **KAN-4, KAN-5, KAN-6** | **Done** after full workflow |

## Jira workflow performed (same Atlassian account JEESUS)

Educational simulated roles on one account (Cursor agent) — **no impersonation of other people**.

For each of KAN-4 / KAN-5 / KAN-6:

1. Created Bug with reproduction + GitHub link  
2. Assigned to JEESUS  
3. Comment: triage / reproduce  
4. Transition → In Progress (`В работе`)  
5. Comment: fix summary + lifecycle path  
6. Transition → Ready for Testing  
7. Comment: Selenium retest PASS  
8. Transition → Done (`Готово`)

## Fixes in lifecycle copy

| SEED | File | Fix |
|---|---|---|
| 001 | `kt04_lifecycle/index.html` | Reject empty password |
| 002 | `kt04_lifecycle/register.html` | Email must match `local@domain.tld` |
| 003 | `kt04_lifecycle/dashboard.html` | Reject `qty <= 0` |

## Before / after

| Defect | BEFORE | AFTER | Jira |
|---|---|---|---|
| Empty password | TC-02 FAIL | retest PASS | KAN-4 Done |
| Invalid email | TC-03 FAIL | retest PASS | KAN-5 Done |
| Qty=0 | TC-04 FAIL | retest PASS | KAN-6 Done |
