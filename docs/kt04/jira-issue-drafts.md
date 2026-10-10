# KT04 — Jira Bug drafts (not yet created in Jira)

Copy into Jira when project `QAKT04` exists. Status in tracker: **DRAFT / BLOCKED**.

## QAKT04-1 — Empty password accepted (SEED-001)

- **Type:** Bug | **Priority:** High | **Component:** Authentication
- **GitHub:** #1
- **Steps / Expected / Actual:** see `bug-reports/bug-reports.md` BUG-KT04-001
- **Environment:** Windows, Chrome, Selenium 4.50, Campus Portal `fixtures/kt04`
- **Evidence:** `screenshots/kt04/tc02_seed001_empty_password.png`
- **Lifecycle fix:** `fixtures/kt04_lifecycle` + `test_lifecycle_empty_password_rejected` **PASS**
- **Suggested comment (implementer = Cursor agent):** Fixed empty-password bypass in lifecycle copy; retest PASS 2026-10-10.

## QAKT04-2 — Email without TLD accepted (SEED-002)

- **Type:** Bug | **Priority:** High | **Component:** Registration
- **GitHub:** #2
- **Evidence:** `screenshots/kt04/tc03_seed002_invalid_email.png`
- **Lifecycle fix:** email regex `local@domain.tld`; retest PASS

## QAKT04-3 — Quantity 0 accepted (SEED-003)

- **Type:** Bug | **Priority:** Medium | **Component:** Order Processing
- **GitHub:** #3
- **Evidence:** `screenshots/kt04/tc04_seed003_zero_quantity.png`
- **Lifecycle fix:** reject `qty <= 0`; retest PASS
