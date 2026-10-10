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

## Components — PARTIAL

| Check | Result |
|---|---|
| Project style | `next-gen` / `simplified: true` |
| Issue UI field «Компоненты» | **Not present** (only «Метки») |
| `GET /rest/api/3/project/KAN/components` | `[]` (empty) |
| Issue `fields.components` on KAN-4/5/6 | `[]` |

**Native Components are not configured / not exposed on this team-managed project.**  
Labels are used as a documented substitute (not claimed as native Components):

| Component (planned) | Label used | Issue |
|---|---|---|
| Authentication | `authentication` | KAN-4 |
| Registration | `registration` | KAN-5 |
| Order Processing | `order-processing` | KAN-6 |

### Proposed native components (not created — needs user approval)

If the teacher requires native Components and the project can enable them:

1. `Authentication`
2. `Registration`
3. `Order Processing`

Do **not** create or assign these without explicit authorization.

## Workflow statuses (actual board columns)

Open (`Открыть`) → In Progress (`В работе`) → **Ready for Testing** → Done (`Готово`)

Verified changelog on KAN-4: Open→In Progress→Ready for Testing→Done.

## Screenshots

Historical:

- `screenshots/kt04/jira/01_board_college_qa.png`
- `screenshots/kt04/jira/02_issue_KAN-4.png`
- `screenshots/kt04/jira/03_filter_bugs_done.png`

Final verification (2026-10-11):

- `screenshots/kt04/jira/final/02_KAN-4_issue_comments.png`
- `screenshots/kt04/jira/final/03_KAN-4_history.png`
- `screenshots/kt04/jira/final/04_project_summary.png`
- `screenshots/kt04/jira/final/05_dashboard_kt04_reports.png`
- `screenshots/kt04/jira/final/06_board_done_bugs.png`
- `screenshots/kt04/jira/final/07_saved_filter_bugs_done.png`
