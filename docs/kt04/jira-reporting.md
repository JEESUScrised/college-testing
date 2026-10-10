# KT04 — Jira reporting (REAL)

Site: https://collegeqakt04.atlassian.net  
Project: KAN — College QA Defect Lifecycle

## Native filter evidence

Filter (UI): Project = College QA Defect Lifecycle, Type = Баг  

URL: https://collegeqakt04.atlassian.net/issues/?jql=project%20%3D%20KAN%20AND%20type%20%3D%20%D0%91%D0%B0%D0%B3%20ORDER%20BY%20key  

Screenshot: `screenshots/kt04/jira/03_filter_bugs_done.png`

## Counts (verified 2026-10-11)

| Metric | Count |
|---|---:|
| Total Bug issues (KAN-4..6) | 3 |
| Open / To Do bugs | 0 |
| In Progress bugs | 0 |
| Ready for Testing bugs | 0 |
| Done / Готово bugs | **3** |
| Priority High | 2 (KAN-4, KAN-5) |
| Priority Medium | 1 (KAN-6) |
| By label authentication | 1 |
| By label registration | 1 |
| By label order-processing | 1 |

## Board / dashboards

Kanban board columns used as workflow progress view:  
https://collegeqakt04.atlassian.net/jira/software/projects/KAN/boards/2  

Custom dashboard gadgets: not required for these three closed bugs; issue navigator filter used as native reporting evidence.

## Limitations

- Project key is **KAN** (not QAKT04) — auto key from onboarding.  
- Components implemented as **labels** (team-managed).  
- Status names partially localized (Открыть / В работе / Готово) with Ready for Testing in English.
