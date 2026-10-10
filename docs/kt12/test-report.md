# KT12 — Отчёт о выполнении

**Дата:** 2026-10-10

## Среда

- grpcio / grpcio-tools **1.84.0**
- protobuf **7.36.2**
- Python 3.13.2, pytest 8.4.2

## Диагностика

`test_tc12_01_create_item_successfully` — **PASS** (0.26 с, collect 10).

## Полный suite

```
============================= 10 passed in 2.34s ==============================
```

JUnit: tests=10, failures=0, errors=0.

## Доказательства статусов (evidence.jsonl)

- `ALREADY_EXISTS` — TC-12-03  
- `INVALID_ARGUMENT` — TC-12-04  
- `NOT_FOUND` — TC-12-05  
- `DEADLINE_EXCEEDED` — TC-12-10  
- streaming: ListItems ids=[s1,s2,s3]; BulkCreate count=3; EchoWatch 3 ответа  

## Артефакты

`grpc/artifacts/kt12/` — pytest log, junit, html, evidence.jsonl, versions_*.json  
Скриншот отчёта: `screenshots/kt12/01_pytest_html_report.png`

## SHA-256 (16 hex)

| Файл | SHA16 |
|---|---|
| pytest_kt12_20261010_135030.log | E656BF1468AA2C30 |
| junit_kt12_20261010_135030.xml | 33F69FACE4CA7013 |
| report_kt12_20261010_135030.html | 7329D8123EB2800D |
