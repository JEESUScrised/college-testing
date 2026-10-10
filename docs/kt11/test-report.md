# КТ 11 — Отчёт о выполнении

**Дата:** 2026-10-10  

## Среда

| Компонент | Версия |
|---|---|
| OS | Windows 10 10.0.19045 |
| Python | 3.13.2 |
| Robot Framework | 7.5 |
| SeleniumLibrary | 6.9.0 |
| Selenium | 4.50.0 |
| Chrome | 155.x |

## Диагностика

Dry-run: **10 tests discovered**, syntax PASS.  
TC-11-01 (отдельный прогон): **PASS**.

## Полный suite

```
10 tests, 10 passed, 0 failed
SUITE PASS elapsed= 28.389725
```

| ID | Статус | elapsed (с) |
|---|---|---|
| TC-11-01 | PASS | 2.74 |
| TC-11-02 | PASS | 2.80 |
| TC-11-03 | PASS | 2.81 |
| TC-11-04 | PASS | 2.81 |
| TC-11-05 | PASS | 2.78 |
| TC-11-06 | PASS | 2.79 |
| TC-11-07 | PASS | 2.80 |
| TC-11-08 | PASS | 2.82 |
| TC-11-09 | PASS | 2.88 |
| TC-11-10 | PASS | 2.77 |

## Артефакты

- `robot/artifacts/kt11/output.xml`
- `robot/artifacts/kt11/log.html`
- `robot/artifacts/kt11/report.html`
- `robot/artifacts/kt11/xunit.xml`
- `screenshots/kt11/01_…` … `12_robot_log.png`

## Команда

```powershell
.\scripts\run_kt11.ps1
# эквивалент:
.\.venv\Scripts\python.exe -m robot --outputdir robot\artifacts\kt11 `
  --output output.xml --log log.html --report report.html --xunit xunit.xml `
  --name "KT11 Robot Framework" robot\tests\kt11.robot
```
