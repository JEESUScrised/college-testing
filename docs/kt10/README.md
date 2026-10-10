# КТ 10 — Кроссбраузерность, отчёты и WebDriver Event Listeners

## Цель

Прогнать одну матрицу сценариев в **Chrome** и **Firefox**, зафиксировать различия через machine-readable summary, подключить **Selenium Event Listener** (`AbstractEventListener` + `EventFiringWebDriver`) и **pytest hooks** (screenshot-on-failure, HTML/JUnit).

Презентация cloud.ithub.ru (КТ10) без логина недоступна — полное соответствие скрытым слайдам не утверждается.

## Среда (факт)

| Компонент | Версия / путь |
|---|---|
| OS | Windows 10 10.0.19045 |
| Python | 3.13.2 (`.venv`) |
| Selenium | 4.50.0 |
| pytest / pytest-html | 8.4.2 / 4.2.0 |
| Chrome | 155.0.8059.39 |
| Firefox | 157.0.1 |

## Отличие listener vs pytest hook

| Механизм | Где | Что делает |
|---|---|---|
| `Kt10EventListener` | WebDriver (`EventFiringWebDriver`) | `before/after_navigate_to`, `before/after_click`, `on_exception` → `events.jsonl` |
| `pytest_runtest_makereport` | pytest | `run_summary.jsonl`, screenshot при FAIL, extras в pytest-html |

## Матрица 5×2

| # | Сценарий | chrome | firefox |
|---|---|---|---|
| 1 | Title + URL + capabilities | PASS | PASS |
| 2 | DOM click | PASS | PASS |
| 3 | Form validation | PASS | PASS |
| 4 | Window switch | PASS | PASS |
| 5 | iframe switch | PASS | PASS |

**Suite:** `10 passed in 52.92s` (лог `pytest_kt10_20261010_132850.log`).

**Failure demo (отдельно):** 1 intentional FAIL → `FAIL_chrome_…png` + `failures.jsonl`.

## Команды

```powershell
.\scripts\diagnose_kt10.ps1
.\scripts\run_kt10.ps1
# или по частям:
.\scripts\run_kt10.ps1 -SkipFailureDemo
.\scripts\run_kt10.ps1 -FailureDemoOnly
```

## Артефакты

- Код: `selenium/crossbrowser/`
- Скриншоты: `screenshots/kt10/`
- Логи/HTML/JUnit/JSONL: `selenium/artifacts/kt10/` (локально; в `.gitignore`)
- Отчёт: `reports/KT10.docx`
