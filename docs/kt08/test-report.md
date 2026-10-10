# Отчёт о тестировании — КТ 08 (remediation)

Дата remediation: **2026-10-10**.

## Среда

| Параметр | Значение |
|---|---|
| Python / Selenium / Pillow | 3.13.2 / 4.50.0 / 11.x |
| allure-pytest | 2.16.2 |
| Allure CLI | 2.37.0 |
| Java | OpenJDK 21 |
| Публичный сайт | https://www.saucedemo.com/ |

## Исторический Pillow suite (сохранён)

```
5 passed in 13.71s
```

## Remediation прогоны

| Прогон | Результат |
|---|---|
| DiagnosticPublic TC-08-P01 | **1 passed in 3.84s** |
| Public only | **4 passed in 21.27s** |
| Full (Pillow + Public) | **9 passed in 34.64s** |

Лог Full: `pytest_kt08_20261010_144813.log` (SHA16 `08CE9954B2C0F07F`).

## Allure

- Results: `selenium/artifacts/kt08/allure-results/` (9 `*-result.json`, PNG attachments в шагах)
- HTML: `selenium/artifacts/kt08/allure-report/index.html`
- UI screenshots: `screenshots/kt08/allure_01_overview.png`, `allure_02_suites.png`
- Public screenshots: `public_01_…` … `public_04_…`

## Compliance (7 требований преподавателя)

См. матрицу в `reports/KT08.docx` и STATUS — все 7 = **PASS** по фактическим артефактам.
