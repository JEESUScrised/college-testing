# Статус контрольных точек

Дата начала: 2026-10-09.

| КТ | Статус | Тесты | Отчёт | Примечания |
|---|---|---|---|---|
| 01 | DONE | PASS | DONE | `reports/KT01.docx` |
| 02 | DONE | PASS | DONE | `reports/KT02.docx` |
| 03 | DONE | PASS | DONE | `reports/KT03.docx` |
| 04 | DONE | MIXED | DONE | seeded FAIL; Issues #1–#3; `reports/KT04.docx` |
| 05 | DONE | MIXED | DONE | VDNH; полный прогон **9 PASS / 1 FAIL** (98.63 с); целевой show_more **PASS** (11.60 с) — отдельно; **не** один прогон 10/10; `reports/KT05.docx` |
| 06 | DONE | PASS | DONE | AVD `Medium_Phone_API_36.1` (API 36); suite **7 PASS** (44.63 с); `reports/KT06.docx` |
| 07 | DONE | PASS | DONE | Grid 4.50 Standalone **5 PASS** (4.88 с); Hub+Node verified; `reports/KT07.docx` |
| 08 | TODO | NOT RUN | TODO | Визуальное сравнение |
| 09 | TODO | NOT RUN | TODO | Свайпы |
| 10 | TODO | NOT RUN | TODO | Браузеры + отчеты |
| 11 | TODO | NOT RUN | TODO | 10 Robot тестов |
| 12 | TODO | NOT RUN | TODO | 10 gRPC тестов |

Значения: TODO / IN PROGRESS / DONE / BLOCKED. Тесты: PASS / FAIL / SKIP / NOT RUN / MIXED.

## КТ 07 — Selenium Grid 4

- JAR: `selenium-server-4.50.0` (SeleniumHQ release; вне Git).
- Скрипты: `selenium/grid/start_standalone.ps1`, `start_hub_node.ps1`, `stop_grid.ps1`, `health_check.ps1`.
- Bind: `127.0.0.1`; Node port **5556** (5555 занят qemu/emulator).
- Event Bus принудительно `tcp://127.0.0.1:4442/4443` (иначе VPN 26.x ломал регистрацию Node).
- Фикстура `grid_driver` (RemoteWebDriver); локальный `driver` KT01–KT05 не изменён.
- Standalone suite: **5 passed in 4.88s**; Hub+Node: node `http://127.0.0.1:5556`, 2 PASS proof.
- Документы: `docs/kt07/`, `selenium/grid/README.md`; отчёт `reports/KT07.docx`.
- Кросс-машинный Grid не разворачивался (честно задокументировано).

## КТ 06 — Appium Android

- Каркас: `mobile/` (pytest + Appium-Python-Client + UiAutomator2Options, Page Object, 7 тест-кейсов ApiDemos).
- Appium 3.8.0 + uiautomator2@8.7.0 (локально в `mobile/node_modules`).
- APK: ApiDemos v6.0.18, SHA-256 `A9EECF37…F686` (вне Git).
- Скрипты: `scripts/diagnose_kt06.ps1`, `start_kt06_services.ps1`, `run_kt06.ps1`, `collect_kt06_artifacts.ps1`.
- Новый ПК: `ANDROID_HOME=C:\Users\user\AppData\Local\Android\Sdk`, JAVA_HOME=Android Studio JBR 21, AVD **`Medium_Phone_API_36.1`** (API 36; `KT06_API33` не создавался — вариант B).
- Аудит: `mobile/environment-report.md` — **READY**.
- Прогоны: диагностика PASS → suite №1 **6/1** (TextFields вне экрана) → scroll-fix → suite №2 **7 PASS / 44.63 с**.
- Скриншоты: `screenshots/kt06/01_*.png` … `08_textfields.png`.
- `reports/KT06.docx` создан по фактическим артефактам.
- KT09 не реализован; среда рассчитана на переиспользование.

## КТ 05 — факт прогонов

### Прогон №1 (полный, без VPN)

- Скрипт: `scripts/run_kt05_no_vpn.ps1`
- Результат: **9 passed, 1 failed in 98.63s**, exit 1
- FAIL: `test_show_more_loads_additional_cards` (`TimeoutException`, wait 35s)
- Артефакты: `selenium/artifacts/kt05/pytest_20261009_125706.log` (+ junit/html/summary)
- Скриншоты: `screenshots/kt05/01_*.png` … `09_before_show_more.png`, `11_*`, `12_*`

### Прогон №2 (только show_more, после правки PO)

- Скрипт: `scripts/run_kt05_show_more_only.ps1`
- Результат: **1 passed in 11.60s**, exit 0
- Артефакты: `selenium/artifacts/kt05/pytest_show_more_20261009_131026.log` (+ junit/html/summary)
- Скриншот: `screenshots/kt05/10_after_show_more.png`

### Вывод по FAIL

- Наиболее вероятно: исправление Page Object (перепоиск кнопки + более широкое условие успеха).
- Неопределённость: полный suite с новым кодом повторно не гонялся.
- Дефект сайта не подтверждён.
- Отчёт: `reports/KT05.docx`. Документы: `docs/kt05/`.

## КТ 04

Campus Portal Demo; 2 PASS / 3 FAIL (seeded); Issues #1–#3 Open; `reports/KT04.docx`.

## КТ 01–03

См. `reports/KT01.docx` … `KT03.docx`.
