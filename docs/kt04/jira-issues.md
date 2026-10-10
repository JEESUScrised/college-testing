# KT04 — Jira issues registry

## Status: BLOCKED — no real Jira issue keys

Checked **2026-10-11**:

| Check | Result |
|---|---|
| Jira / Atlassian MCP connector | Not available |
| Env `JIRA_*` / `ATLASSIAN_*` credentials | Not set (values not printed) |
| Browser session | Opened `https://id.atlassian.com/login` → **login page** (not authenticated) |
| Real issue keys | **None** — not invented |

Until the user signs in to Atlassian and **explicitly approves** creating project `QAKT04` and three Bug issues, this file must not contain fabricated keys.

## Planned mapping (after creation)

| Local ID | Planned Jira key | Summary | Component | Priority | GitHub |
|---|---|---|---|---|---|
| BUG-KT04-001 | *(pending)* | Empty password accepted | Authentication | High | #1 |
| BUG-KT04-002 | *(pending)* | Email without TLD accepted | Registration | High | #2 |
| BUG-KT04-003 | *(pending)* | Quantity 0 accepted | Order Processing | Medium | #3 |

Full draft bodies: `docs/kt04/jira-issue-drafts.md`, `bug-reports/bug-reports.md`.  
CSV import template: `docs/kt04/jira-import-bugs.csv`.

## Verification checklist (when unblocked)

For each created issue, re-fetch via UI/API and record:

- [ ] Issue key (real)
- [ ] Project = QAKT04 (or actual key)
- [ ] Type = Bug
- [ ] Priority / component
- [ ] Steps readable
- [ ] Attachment or screenshot link
- [ ] Status after transitions
