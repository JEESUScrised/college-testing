# KT04 — Jira reporting (NATIVE, configured 2026-10-11)

Site: https://collegeqakt04.atlassian.net  
Project: KAN — College QA Defect Lifecycle

## Counts (REST re-verified)

| Metric | Count | Keys |
|---|---:|---|
| Total Bug defects | **3** | KAN-4, KAN-5, KAN-6 |
| Open defects | **0** | — |
| Closed / Done defects | **3** | KAN-4, KAN-5, KAN-6 |
| Priority High | **2** | KAN-4, KAN-5 |
| Priority Medium | **1** | KAN-6 |

## Saved filter

- Name: **KT04 KAN Bugs Done**
- URL: https://collegeqakt04.atlassian.net/issues/?filter=10002
- JQL: `project = KAN AND type = Баг ORDER BY key`
- Screenshot: `screenshots/kt04/jira/final/07_saved_filter_bugs_done.png`

## Dashboard (configured)

- Name: **KT04 Defect Reports**
- URL: https://collegeqakt04.atlassian.net/jira/dashboards/10001
- Screenshot: `screenshots/kt04/jira/final/08_dashboard_configured_stats.png`

| Gadget | Live content |
|---|---|
| Bugs by Status | ГОТОВО = **3** (100%) |
| Bugs by Priority | High = **2** (67%), Medium = **1** (33%) |
| Priority × Status | Done×High=2, Done×Medium=1 |
| KAN Bugs (filter results) | KAN-4, KAN-5, KAN-6 listed |

Gadgets use saved filter `10002`.

## Project Summary

URL: https://collegeqakt04.atlassian.net/jira/software/projects/KAN/summary  
Screenshot: `screenshots/kt04/jira/final/04_project_summary.png`

## Components breakdown

**N/A** — native Components unavailable on team-managed KAN (POST 405).  
Label distribution (substitute): authentication=1, registration=1, order-processing=1.

## Status of reporting requirement

**PASS** for filter + configured dashboard charts + summary counts.  
**PARTIAL** only for Components breakdown (platform limitation).
