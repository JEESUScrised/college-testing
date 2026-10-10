# Campus Portal — lifecycle remediation copy

Original defective fixtures remain in `selenium/fixtures/kt04/` (historical seeded FAIL evidence).

This directory contains **fixed** validation for SEED-001/002/003 used to demonstrate
retest-after-fix for KT04 Jira lifecycle (without rewriting history).

| Seed | Fix |
|---|---|
| SEED-001 | Reject empty password |
| SEED-002 | Require email `local@domain.tld` |
| SEED-003 | Reject quantity ≤ 0 |
