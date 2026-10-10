# KT04 — Defect lifecycle (local + REAL Jira)

## Layers

| Layer | Location | Status |
|---|---|---|
| Historical seeded app | `selenium/fixtures/kt04/` | Unchanged; **2 PASS / 3 FAIL** |
| Lifecycle fixed copy | `selenium/fixtures/kt04_lifecycle/` | SEED-001/002/003 fixed |
| Selenium retest | `test_kt04_lifecycle_retest.py` | **3 PASS / 8.74s** (2026-10-11) |
| GitHub Issues | #1–#3 | Preserved Open (historical) |
| Jira Issues | **KAN-4, KAN-5, KAN-6** | **Done** (remote verified) |

## Mapping: defect → Jira → fix → retest → Done

| Seed | Defect | Jira | App fix path | Retest | Final Jira |
|---|---|---|---|---|---|
| SEED-001 | Empty password accepted | KAN-4 | `kt04_lifecycle/index.html` | PASS | Done |
| SEED-002 | Email without TLD accepted | KAN-5 | `kt04_lifecycle/register.html` | PASS | Done |
| SEED-003 | Quantity zero accepted | KAN-6 | `kt04_lifecycle/dashboard.html` | PASS | Done |

Original seeded fixtures were **not** modified. Fixes live only in `kt04_lifecycle/`.

## Jira workflow performed (account JEESUS)

Educational simulated roles on one account — **no impersonation of other people**.

For each of KAN-4 / KAN-5 / KAN-6:

1. Created Bug with reproduction + GitHub link  
2. Assigned to JEESUS  
3. Comment: triage / reproduce  
4. Transition → In Progress (`В работе`)  
5. Comment: fix summary + lifecycle path  
6. Transition → Ready for Testing  
7. Comment: Selenium retest PASS  
8. Transition → Done (`Готово`)

KAN-4 changelog (REST): Open → In Progress → Ready for Testing → Done.

## Before / after

| Defect | BEFORE (seeded) | AFTER (lifecycle) | Jira |
|---|---|---|---|
| Empty password | TC-02 FAIL | retest PASS | KAN-4 Done |
| Invalid email | TC-03 FAIL | retest PASS | KAN-5 Done |
| Qty=0 | TC-04 FAIL | retest PASS | KAN-6 Done |
