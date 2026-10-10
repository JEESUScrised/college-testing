# Сводка по дефектам — КТ 04

## Статистика

| Метрика | Значение |
|---|---:|
| Тест-кейсов (seeded suite) | 5 |
| PASS (seeded) | 2 |
| FAIL (выявили seeded-баги) | 3 |
| Подтверждённых дефектов | 3 |
| Issues в GitHub | 3 (#1, #2, #3) |
| Issues в Jira | **0** (BLOCKED) |
| Lifecycle retest PASS | **3** (8.74 с, 2026-10-11) |
| Closed в Jira | 0 |

## Связь дефект ↔ тест ↔ трекер

| Bug ID | Seed | Тест | GitHub | Jira | Severity | Seeded status | Lifecycle |
|---|---|---|---|---|---|---|---|
| BUG-KT04-001 | SEED-001 | TC-02 FAIL | [#1](https://github.com/JEESUScrised/college-testing/issues/1) | *не создан* | Major | Open | Fixed in copy + retest PASS |
| BUG-KT04-002 | SEED-002 | TC-03 FAIL | [#2](https://github.com/JEESUScrised/college-testing/issues/2) | *не создан* | Major | Open | Fixed in copy + retest PASS |
| BUG-KT04-003 | SEED-003 | TC-04 FAIL | [#3](https://github.com/JEESUScrised/college-testing/issues/3) | *не создан* | Minor | Open | Fixed in copy + retest PASS |

## Жизненный цикл

| Шаг | GitHub | Local lifecycle app | Jira |
|---|---|---|---|
| Open / reproduce | Done (#1–#3) | Seeded FAIL preserved | BLOCKED |
| In Progress / fix | N/A | Fixed in `kt04_lifecycle/` | BLOCKED |
| Retest | N/A | **3 PASS** | BLOCKED |
| Done / Closed | Issues remain Open (historical) | Verified | BLOCKED |

## Labels в GitHub

`bug`, `kt04`, `educational`, `severity:major` / `severity:minor`, `priority:high` / `priority:medium`.
