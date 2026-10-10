# KT04 — Jira project design (College QA Defect Lifecycle)

## Status: BLOCKED — no authorized Jira workspace access

Rechecked **2026-10-11**:

1. No Atlassian/Jira MCP tools in this agent session.
2. No `JIRA_*` / `ATLASSIAN_*` environment credentials configured.
3. Cursor browser opened `https://id.atlassian.com/login` → **Atlassian login page** (not signed in).

**No real Jira project, issues, comments, assignments, transitions, or native reports were created.**  
Creating them requires: user login in the legitimate Atlassian UI **and** explicit approval to create/modify Jira resources.

## Planned project (ready when authorized)

| Field | Value |
|---|---|
| Name | College QA Defect Lifecycle |
| Key | `QAKT04` (or next available) |
| Type | Software / Kanban if supported |
| Components | Authentication, Registration, Order Processing |
| Issue types | Bug, Task, Improvement |
| Priorities | Highest / High / Medium / Low (site defaults OK) |

## Planned workflow states

Open → In Progress → Ready for Testing → Done  

(Use only states the account actually supports; do not claim custom states until configured.)

## Actual recorded configuration

| Item | Value |
|---|---|
| Workspace URL | *not available — not logged in* |
| Project URL | *not created* |
| Project key | *not created* |
| Issue types / components / workflow | *not configured* |

## Cross-reference

Historical GitHub Issues (preserved):

- https://github.com/JEESUScrised/college-testing/issues/1
- https://github.com/JEESUScrised/college-testing/issues/2
- https://github.com/JEESUScrised/college-testing/issues/3

Local lifecycle fixes: `selenium/fixtures/kt04_lifecycle/` — retest **3 PASS / 8.74s** (2026-10-11).

## User action required

1. Sign in at `https://id.atlassian.com/login` (Cursor browser or system browser).
2. Explicitly authorize creating project `QAKT04` (or alternative key).
3. Approve creating three Bug issues from `jira-issue-drafts.md` / `jira-import-bugs.csv`.
4. Approve workflow transitions and comments for the educational lifecycle demo.
5. Re-run the agent to complete real Jira evidence + screenshots.
