# KT04 — Jira reporting

## Status: BLOCKED

Native Jira filters, dashboards, and project reports **cannot** be produced without a real project.

| Desired report | Status |
|---|---|
| Total defects | N/A — 0 Jira issues exist |
| Open / In Progress / Done | N/A |
| By priority | N/A |
| By component | N/A |
| Workflow progress | N/A |

Do **not** treat local Markdown tables or charts as native Jira reports.

## Planned filters (when QAKT04 exists)

- `project = QAKT04 AND type = Bug`
- `project = QAKT04 AND statusCategory != Done`
- `project = QAKT04 AND priority in (High, Highest)`
- `project = QAKT04 AND component = "Authentication"`

## Local educational statistics (not Jira-native)

| Source | Open bugs | Closed bugs |
|---|---|---|
| GitHub Issues #1–#3 | 3 | 0 |
| Lifecycle Selenium retest | defects fixed in copy | verified 3/3 PASS |

## After unblocking

Capture real screenshots of:

1. Project board / issue list  
2. At least one filter result  
3. Any available dashboard gadget  

Store under `screenshots/kt04/jira/` (create only with real captures).
