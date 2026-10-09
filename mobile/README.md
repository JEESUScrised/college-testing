# Mobile testing (KT06 / подготовка к KT09)

Автоматизация UI Android через **Appium 3** + **UiAutomator2** + **Appium-Python-Client** на официальном приложении [ApiDemos](https://github.com/appium/android-apidemos).

## Структура

```
mobile/
  apps/                  # ApiDemos-debug.apk (не в Git) + README с SHA-256
  pages/                 # Page Object
  tests/test_kt06_appium.py
  conftest.py            # session-scoped driver, UiAutomator2Options
  requirements.txt
  package.json           # appium@3.8.0 + uiautomator2
  environment-report.md  # аудит среды
  docs/                  # план / кейсы / отчёт
  artifacts/             # junit, pytest log, appium log (gitignore)
```

## Требования

1. Node.js `^20.19.0 || ^22.12.0 || >=24.0.0`, npm ≥ 10  
2. Java JDK 17+, `JAVA_HOME`  
3. Android SDK: `ANDROID_HOME`, platform-tools, emulator  
4. **AVD или физическое устройство** (обязательно для прогона)  
5. Python 3.13 + `.venv` с `mobile/requirements.txt`

Аудит: `.\scripts\diagnose_kt06.ps1` → `mobile/environment-report.md`.

## Установка (один раз)

```powershell
cd mobile
npm install
npx appium driver install uiautomator2
cd ..
.\.venv\Scripts\python.exe -m pip install -r mobile\requirements.txt
# APK:
cd mobile\apps
Invoke-WebRequest -Uri "https://github.com/appium/android-apidemos/releases/download/v6.0.18/ApiDemos-debug.apk" -OutFile ApiDemos-debug.apk
Get-FileHash .\ApiDemos-debug.apk -Algorithm SHA256
```

## Запуск

```powershell
.\scripts\diagnose_kt06.ps1
.\scripts\start_kt06_services.ps1   # эмулятор (если нужно) + Appium :4723
.\scripts\run_kt06.ps1              # один прогон pytest
.\scripts\collect_kt06_artifacts.ps1
```

Endpoint Appium по умолчанию: `http://127.0.0.1:4723`.

Эмулятор **не** перезапускается между тестами: одна session-scoped сессия, между тестами — `mobile: startActivity` на home.

## Тест-кейсы (7)

| # | Имя | Что проверяет |
|---|---|---|
| 1 | `test_app_starts_and_shows_home` | Старт ApiDemos, список разделов |
| 2 | `test_navigate_to_app_menu` | Home → App |
| 3 | `test_open_alert_dialogs_screen` | App → Alert Dialogs |
| 4 | `test_list_dialog_interaction` | List dialog + выбор пункта |
| 5 | `test_text_entry_dialog_input` | Text Entry: ввод username |
| 6 | `test_back_returns_to_previous_screen` | Back на предыдущий экран |
| 7 | `test_views_textfields_input` | Views → TextFields ввод |

## KT09

Та же среда (Appium, APK, venv, эмулятор, скрипты). KT09 **не** реализован здесь.

## Статус на момент scaffold

См. `environment-report.md`: без AVD/устройства прогон **BLOCKED**. `reports/KT06.docx` создаётся **только** после реального успешного/частичного прогона.
