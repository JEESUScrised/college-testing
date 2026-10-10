# KT04 — Jira issues registry (REMOTE VERIFIED)

## Status: CREATED AND REMOTELY VERIFIED (2026-10-11)

Site: https://collegeqakt04.atlassian.net  
Project: College QA Defect Lifecycle (**KAN**)

Verification method: authenticated browser session + Jira REST (`/rest/api/3/issue/{key}`, changelog).  
No tokens or cookies are stored in the repository.

| Local ID | Jira key | Summary | Type | Priority | Labels | Assignee | Final status | URL |
|---|---|---|---|---|---|---|---|---|
| BUG-KT04-001 | **KAN-4** | Login accepts empty password | Баг | High | authentication, educational, kt04, seed-001 | JEESUS | Готово (Done) | https://collegeqakt04.atlassian.net/browse/KAN-4 |
| BUG-KT04-002 | **KAN-5** | Registration accepts email without TLD | Баг | High | registration, educational, kt04, seed-002 | JEESUS | Готово (Done) | https://collegeqakt04.atlassian.net/browse/KAN-5 |
| BUG-KT04-003 | **KAN-6** | Order accepts quantity zero | Баг | Medium | order-processing, educational, kt04, seed-003 | JEESUS | Готово (Done) | https://collegeqakt04.atlassian.net/browse/KAN-6 |

GitHub originals preserved: #1, #2, #3.

## REST verification checklist

- [x] Issues exist in project KAN (keys KAN-4/5/6)
- [x] Type = Баг
- [x] Priority High / High / Medium
- [x] Reproduction text in description (steps / expected / actual / evidence)
- [x] Labels used for component mapping (`components` field empty)
- [x] Assignee = JEESUS
- [x] Status Done / Готово
- [x] Comments present (**3 per issue**: triage / fix / retest)
- [x] Status history includes Open → In Progress → Ready for Testing → Done (KAN-4 changelog)

## Do not recreate

These issues already exist. Creating duplicates is forbidden.
