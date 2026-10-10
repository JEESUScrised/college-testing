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
| 08 | DONE | PASS | DONE | Pillow visual regression; suite **5 PASS** (13.71 с); `reports/KT08.docx` |
| 09 | DONE | PASS | DONE | Appium gestures Android; suite **5 PASS** (54.93 с); iOS NOT RUN; `reports/KT09.docx` |
| 10 | DONE | PASS | DONE | Chrome×Firefox 5×2 **10 PASS** (52.92 с); listeners+HTML/JUnit; `reports/KT10.docx` |
| 11 | DONE | PASS | DONE | Robot Framework 7.5 + SeleniumLibrary; **10 PASS** (28.39 с); `reports/KT11.docx` |
| 12 | DONE | PASS | DONE | Inventory gRPC; **10 PASS** (2.34 с); `reports/KT12.docx` |

Значения: TODO / IN PROGRESS / DONE / BLOCKED. Тесты: PASS / FAIL / SKIP / NOT RUN / MIXED.

## Итог проекта (КТ 01–12)

Все 12 контрольных точек реализованы; отчёты `reports/KT01.docx` … `reports/KT12.docx` присутствуют.

Известные ограничения (сохранены):
- **КТ04** — намеренные seeded FAIL / MIXED.
- **КТ05** — полный прогон 9 PASS / 1 FAIL; show_more отдельно PASS (не один прогон 10/10).
- **КТ09** — только Android; iOS NOT RUN.
- Презентации cloud.ithub.ru без логина недоступны — полное соответствие скрытым слайдам не утверждается.

## КТ 12 — gRPC InventoryService (финальная)

- grpcio/grpcio-tools **1.84.0**, protobuf **7.36.2**; proto3 `inventory.proto` + generated stubs.
- Suite: **10 passed in 2.34s**; unary + server/client/bidi streaming + DEADLINE_EXCEEDED.
- Код: `grpc/server/`, `grpc/client/cli.py`, `grpc/tests/test_kt12_grpc.py`, `grpc/conftest.py`.
- Артефакты: `grpc/artifacts/kt12/` (gitignore); скриншот `screenshots/kt12/`; отчёт `reports/KT12.docx`.

## КТ 11 — Robot Framework

- Robot Framework **7.5** + SeleniumLibrary **6.9.0**; Selenium 4.50.0 сохранён.
- Suite: **10 passed / 0 failed**, elapsed **28.39 с** (`output.xml`).
- Код: `robot/tests/kt11.robot`, `robot/resources/*.resource`, `robot/fixtures/`, `robot/lib/FixtureServer.py`.
- Артефакты: `robot/artifacts/kt11/` (gitignore); скриншоты `screenshots/kt11/`; отчёт `reports/KT11.docx`.
- Презентация cloud.ithub.ru недоступна без логина — соответствие скрытым слайдам не утверждается.

## КТ 10 — Кроссбраузерность, отчёты, listeners

- Матрица: Chrome 155.0.8059.39 × Firefox 157.0.1; 5 сценариев × 2 = **10 PASS / 52.92 с**.
- Инфра: `selenium/crossbrowser/` (`EventFiringWebDriver` + `Kt10EventListener`, отдельный `kt10_driver`).
- Отчёты: pytest-html + JUnit; `events.jsonl`, `run_summary.jsonl`, `browser_comparison.json`.
- Failure demo: намеренный FAIL → `FAIL_chrome_….png` (screenshot-on-failure).
- Скриншоты: `screenshots/kt10/`; документы: `docs/kt10/`; отчёт `reports/KT10.docx`.
- Презентация cloud.ithub.ru недоступна без логина — соответствие скрытым слайдам не утверждается.

## КТ 09 — Жесты Appium (Android; iOS не выполнялся)

- Жесты: `mobile/gestures/` (`swipeGesture`/`scrollGesture`, GesturePort).
- Экраны: ApiDemos Views (vertical) + Gallery/1. Photos (horizontal).
- AVD: `Medium_Phone_API_36.1` (API 36); Appium 3.8.0 / uiautomator2 8.7.0.
- Suite: **5 passed in 54.93s**; скриншоты `screenshots/kt09/01_…` … `11_…`.
- iOS / XCUITest: **NOT RUN** (документировано в `mobile/docs/kt09-platform-compatibility.md`).
- Презентация cloud.ithub.ru недоступна без логина — соответствие скрытым слайдам не утверждается.
- Отчёт: `reports/KT09.docx`.

## КТ 08 — Visual regression (Selenium + Pillow)

- Утилита: `selenium/visual/compare.py` (tolerance, diff%, mask/overlay, без auto-resize/auto-baseline).
- Baseline: `selenium/baselines/kt08/home_baseline.png` (Chrome, 1384×849).
- Фикстуры: `selenium/fixtures/kt08/*.html` (локальные, без VDNH).
- Suite: **5 passed in 13.71s** — match 0%; text/color 1.11%; layout 5.06%; significant 99.85%; dimension mismatch 1384×849 vs 884×549.
- Артефакты: `screenshots/kt08/`, `selenium/artifacts/kt08/`; отчёт `reports/KT08.docx`.
- Презентация cloud.ithub.ru недоступна без логина — соответствие скрытым слайдам не утверждается.

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
