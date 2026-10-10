# KT04 — Jira project (REAL, remotely verified 2026-10-11)

## Status: VERIFIED

| Field | Actual value |
|---|---|
| Workspace / site | https://collegeqakt04.atlassian.net |
| Organization | prilepov2005 |
| Account | JEESUS (`prilepov2005@gmail.com`) |
| Project name | College QA Defect Lifecycle |
| Project key | **KAN** (auto-assigned; planned `QAKT04` unavailable) |
| Project URL | https://collegeqakt04.atlassian.net/jira/software/projects/KAN/boards/2 |
| Type | Team-managed (next-gen / simplified) software / Kanban |
| Plan | Cloud Standard trial |
| Project id | 10001 |

Remote verification JSON: `docs/kt04/jira-remote-verification.json`

## Issue types (configured)

Epic, Story, Task, **Баг (Bug)**, Subtask  

Bug was added via Project settings → Типы задач → Добавить тип задачи.

## Priorities

Highest / High / Medium / Low / Lowest (site defaults). Used **High** (KAN-4, KAN-5) and **Medium** (KAN-6).

## Components — UNAVAILABLE on this project type

Investigation (2026-10-11):

| Check | Result |
|---|---|
| Project style | `next-gen` / `simplified: true` |
| Issue UI field «Компоненты» | **Not present** (only «Метки») |
| Issue `editmeta.components` | **null** (field not editable) |
| `GET /rest/api/3/project/KAN/components` | `[]` |
| `POST /rest/api/3/project/KAN/components` | **405 Method Not Allowed** |
| Project settings sidebar | No «Компоненты» admin entry |

**Native Components cannot be created or assigned on this team-managed KAN project.**  
Project was **not** migrated/recreated solely to obtain Components.

Labels remain the documented substitute (not claimed as native Components):

| Area (teacher intent) | Label used | Issue |
|---|---|---|
| Authentication | `authentication` | KAN-4 |
| Registration | `registration` | KAN-5 |
| Order Processing | `order-processing` | KAN-6 |

Proposed native names (`Authentication`, `Registration`, `Order Processing`) are **not applicable** here — API rejects creation.

## Workflow statuses (actual board columns)

Open (`Открыть`) → In Progress (`В работе`) → **Ready for Testing** → Done (`Готово`)

Verified changelog on KAN-4: Open→In Progress→Ready for Testing→Done.

## Screenshots

Historical:

- `screenshots/kt04/jira/01_board_college_qa.png`
- `screenshots/kt04/jira/02_issue_KAN-4.png`
- `screenshots/kt04/jira/03_filter_bugs_done.png`

Final verification:

- `screenshots/kt04/jira/final/02_KAN-4_issue_comments.png`
- `screenshots/kt04/jira/final/03_KAN-4_history.png`
- `screenshots/kt04/jira/final/04_project_summary.png`
- `screenshots/kt04/jira/final/05_dashboard_kt04_reports.png` (pre-config)
- `screenshots/kt04/jira/final/07_saved_filter_bugs_done.png`
- `screenshots/kt04/jira/final/08_dashboard_configured_stats.png` (**live charts**)
