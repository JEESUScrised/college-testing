# KT10 — фактические результаты

Дата прогона: **2026-10-10**.

## Диагностика

```
chrome_ok chrome 155.0.8059.39
firefox_ok firefox 157.0.1
DIAGNOSE_PASS
```

Лог: `selenium/artifacts/kt10/diagnose_kt10_20261010_132721.log`

## Матрица (PASS)

```
============================= 10 passed in 52.92s =============================
```

- JUnit: `junit_kt10_20261010_132850.xml`
- HTML: `report_kt10_20261010_132850.html`
- Log: `pytest_kt10_20261010_132850.log`
- Comparison: `browser_comparison.json` → chrome 5/5, firefox 5/5
- Listener: `events.jsonl` (42 строки; navigate/click по обоим браузерам)

### SHA-256 (первые 16 hex)

| Файл | SHA16 |
|---|---|
| pytest_kt10_20261010_132850.log | 9AFEE07DB0579749 |
| junit_kt10_20261010_132850.xml | AF61A3C26670DAA7 |
| report_kt10_20261010_132850.html | 2EECC6FA5AE7E63B |
| events.jsonl | 285CA756AF6B7C0F |
| browser_comparison.json | E286025F32234CE0 |

## Failure demo (ожидаемый FAIL)

```
FAILED ... test_intentional_failure_for_screenshot_hook[chrome]
1 failed in 2.97s
```

Скриншот: `screenshots/kt10/FAIL_chrome_test_intentional_failure_for_screenshot_hook[chrome].png` (1384×849).

## Скриншоты матрицы

По 8 PNG на браузер: `chrome_01_…` … `chrome_08_…`, `firefox_01_…` … `firefox_08_…`.
Размеры home: Chrome 1384×849, Firefox 1384×907 (разный chrome/Gecko viewport chrome).
