# KT04 — Jira reporting (NATIVE, verified 2026-10-11)

Site: https://collegeqakt04.atlassian.net  
Project: KAN — College QA Defect Lifecycle

## What counts as native reporting here

| Mechanism | Available | Evidence |
|---|---|---|
| Saved filter (Issue Navigator) | **Yes** | Filter id **10002** «KT04 KAN Bugs Done» |
| Project Summary | **Yes** | Completed: **3** (last 7 days) |
| Dashboard | **Yes (shell)** | Dashboard id **10001** «KT04 Defect Reports» — gadgets added, UI still shows «not configured» until filter is selected in Edit |
| Classic board Reports tab | **No** | `/boards/2/reports` → not-found on this team-managed board |
| Native Components breakdown | **No** | Components unavailable; label breakdown used instead |

Do **not** present a locally generated chart as a built-in Jira report.

## Saved filter (primary native report)

- Name: **KT04 KAN Bugs Done**
- URL: https://collegeqakt04.atlassian.net/issues/?filter=10002
- JQL: `project = KAN AND type = Баг ORDER BY key`
- Screenshot: `screenshots/kt04/jira/final/07_saved_filter_bugs_done.png`

## Counts (REST JQL, verified)

| Metric | Count | Keys |
|---|---:|---|
| Total Bug defects | **3** | KAN-4, KAN-5, KAN-6 |
| Open defects (statusCategory ≠ Done) | **0** | — |
| Closed / Done defects | **3** | KAN-4, KAN-5, KAN-6 |
| Priority High | **2** | KAN-4, KAN-5 |
| Priority Medium | **1** | KAN-6 |
| Label authentication | **1** | KAN-4 |
| Label registration | **1** | KAN-5 |
| Label order-processing | **1** | KAN-6 |

## Project Summary

URL: https://collegeqakt04.atlassian.net/jira/software/projects/KAN/summary  
Screenshot: `screenshots/kt04/jira/final/04_project_summary.png`  
Shows native tiles including **Выполнено: 3**.

## Dashboard

URL: https://collegeqakt04.atlassian.net/jira/dashboards/10001  
Screenshot: `screenshots/kt04/jira/final/05_dashboard_kt04_reports.png`  

Gadgets present: Bugs by Status, KAN Bugs, Priority × Status, Bugs by Priority.  
**Limitation:** gadget preferences require UI Edit → select filter `10002` (REST property write did not fully activate charts). Dashboard is native Jira infrastructure; charts are PARTIAL until configured in UI.

## Board

URL: https://collegeqakt04.atlassian.net/jira/software/projects/KAN/boards/2  
Columns: Open / In Progress / Ready for Testing / Done — KAN-4/5/6 in Done.

## Status of reporting requirement

**PARTIAL → mostly PASS for filters/summary/counts; PARTIAL for configured dashboard gadgets and Components breakdown.**

Overall KT04 reporting evidence is sufficient for submission if Components limitation is disclosed.
