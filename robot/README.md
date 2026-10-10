# KT11 — Automated Testing with Robot Framework

Ровно **10** тест-кейсов на native `.robot` синтаксисе + SeleniumLibrary (Chrome).

## Версии

| Пакет | Версия |
|---|---|
| Robot Framework | 7.5 |
| SeleniumLibrary | 6.9.0 |
| Selenium | 4.50.0 (как в KT01–KT10) |
| Python | 3.13.2 |

Установка в существующий `.venv`:

```powershell
.\.venv\Scripts\pip.exe install -r robot\requirements.txt
```

## Структура

```
robot/
  fixtures/          # локальное HTML-приложение
  lib/FixtureServer.py
  resources/common.resource
  resources/pages.resource
  tests/kt11.robot
  artifacts/kt11/    # output.xml, log.html, report.html, xunit.xml
  requirements.txt
```

## Команды

```powershell
# Синтаксис / discovery
.\scripts\run_kt11.ps1 -DryRun

# Один диагностический тест (TC-11-01)
.\scripts\run_kt11.ps1 -DiagnosticOnly

# Полный suite
.\scripts\run_kt11.ps1
```

Скриншоты: `screenshots/kt11/`. Screenshot-on-failure: `SeleniumLibrary run_on_failure=Capture Page Screenshot`.
