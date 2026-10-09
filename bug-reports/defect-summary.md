# Сводка по дефектам — КТ 04

## Статистика

| Метрика | Значение |
|---|---:|
| Тест-кейсов выполнено | 5 |
| PASS | 2 |
| FAIL (выявили seeded-баги) | 3 |
| Подтверждённых дефектов | 3 |
| Issues в GitHub | 3 (#1, #2, #3) |
| Resolved / Closed | 0 (исправления не выполнялись) |

## Связь дефект ↔ тест ↔ issue

| Bug ID | Seed | Тест | Issue | Severity | Status |
|---|---|---|---|---|---|
| BUG-KT04-001 | SEED-001 | TC-02 FAIL | [#1](https://github.com/JEESUScrised/college-testing/issues/1) | Major | Open |
| BUG-KT04-002 | SEED-002 | TC-03 FAIL | [#2](https://github.com/JEESUScrised/college-testing/issues/2) | Major | Open |
| BUG-KT04-003 | SEED-003 | TC-04 FAIL | [#3](https://github.com/JEESUScrised/college-testing/issues/3) | Minor | Open |

## Жизненный цикл дефекта

Типовой цикл в баг-трекере:

1. **Open** — дефект обнаружен, воспроизведён, оформлен (текущий статус всех трёх багов).
2. **In Progress** — разработчик взял задачу в работу.
3. **Resolved** — исправление внесено, ожидается ретест.
4. **Closed** — ретест подтвердил исправление.

Для КТ 04 шаги 2–4 **не выполнялись**: приложение оставлено с учебными seeded-багами,
поэтому все issues остаются в статусе **Open**.

## Labels в GitHub

`bug`, `kt04`, `educational`, `severity:major` / `severity:minor`, `priority:high` / `priority:medium`.
