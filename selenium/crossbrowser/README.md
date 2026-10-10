# KT10 — Cross-Browser Testing, Reporting, WebDriver Listeners

Матрица **Chrome × Firefox** (5 сценариев × 2 браузера = 10 тестов).

## Состав

| Путь | Назначение |
|---|---|
| `listener.py` | `Kt10EventListener` (`AbstractEventListener`) → `artifacts/kt10/events.jsonl` |
| `http_server.py` | Локальный HTTP для `selenium/fixtures/` |
| `conftest.py` | `kt10_driver` = `EventFiringWebDriver`; pytest hook screenshot-on-failure |
| `tests/test_kt10_matrix.py` | 5 сценариев × chrome/firefox |
| `tests/test_kt10_failure_demo.py` | Намеренный FAIL (отдельно от матрицы) |

Корневой `selenium/conftest.py` / фикстура `driver` (КТ01–08) **не заменяются**.

## Зависимости

- Python 3 + `.venv`: `selenium`, `pytest`, `pytest-html`
- Google Chrome + Mozilla Firefox (локально)

## Команды

```powershell
# Диагностика браузеров
.\scripts\diagnose_kt10.ps1

# Матрица 5×2 + controlled failure demo
.\scripts\run_kt10.ps1

# Только матрица
.\scripts\run_kt10.ps1 -SkipFailureDemo

# Только failure demo
.\scripts\run_kt10.ps1 -FailureDemoOnly
```

Или напрямую:

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\crossbrowser\tests\test_kt10_matrix.py -v --tb=short `
  --junitxml=selenium\artifacts\kt10\junit.xml `
  --html=selenium\artifacts\kt10\report.html --self-contained-html
```

## Артефакты

- `selenium/artifacts/kt10/` — pytest log, HTML, JUnit, `events.jsonl`, `run_summary.jsonl`, `browser_comparison.json`
- `screenshots/kt10/` — скриншоты по браузеру; `FAIL_*` при падении

## Сценарии матрицы

1. Title + URL + capabilities  
2. DOM click  
3. Form validation  
4. Window switch (фикстуры KT02)  
5. iframe switch (фикстуры KT02)  
