# Статус контрольных точек

Дата начала: 2026-10-09.

| КТ | Статус | Тесты | Отчёт | Примечания |
|---|---|---|---|---|
| 01 | DONE | PASS | DONE | `reports/KT01.docx` |
| 02 | DONE | PASS | DONE | Local windows/iframe 6 PASS + public Sauce **11 PASS** (49.34 с); `reports/KT02.docx` |
| 03 | DONE | PASS | DONE | Local PO 4 PASS + public Sauce PO **5 PASS** (21.11 с); `reports/KT03.docx` |
| 04 | DONE | MIXED | DONE | seeded 2P/3F + GitHub #1–#3; lifecycle retest **3 PASS**; Jira **BLOCKED**; `reports/KT04.docx` |
| 05 | DONE | MIXED | DONE | VDNH; полный прогон **9 PASS / 1 FAIL** (98.63 с); целевой show_more **PASS** (11.60 с) — отдельно; **не** один прогон 10/10; `reports/KT05.docx` |
| 06 | DONE | PASS | DONE | AVD `Medium_Phone_API_36.1` (API 36); suite **7 PASS** (44.63 с); `reports/KT06.docx` |
| 07 | DONE | PASS | DONE | Standalone 5 PASS + Hub+**2 Nodes** Chrome/Firefox **4 PASS** (7.72 с) + parallel overlap; `reports/KT07.docx` |
| 08 | DONE | PASS | DONE | Public Sauce Demo + Allure; Full **9 PASS** (34.64 с); Pillow history 5/13.71с; `reports/KT08.docx` |
| 09 | DONE | MIXED | DONE | Gestures 5 PASS + BASIC web Win/Android DOM **PASS**; manual checklist PENDING; iOS NOT RUN; `reports/KT09.docx` |
| 10 | DONE | PASS | DONE | Functional 10/52.92с + responsive Sauce **6 PASS** (42.73 с, 36 rows); `reports/KT10.docx` |
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

## КТ 10 — Кроссбраузерность + responsive (remediation 2026-10-10)

- Исторический functional: Chrome×Firefox 5×2 = **10 PASS / 52.92 с** + listener (сохранён).
- Новое: Sauce Demo responsive **6 PASS / 42.73 с** (36 matrix rows; overflow не найден).
- CDP Chrome tablet/phone; Firefox = window resize (не Android/iOS).
- `screenshots/kt10/responsive/`; `reports/KT10.docx` обновлён.

## КТ 09 — Жесты + BASIC cross-platform (remediation 2026-10-10)

- Жесты Android: **5 PASS / 54.93 с** (сохранены).
- BASIC public web auto: Windows Chrome/Firefox **2 PASS**; Android Chrome DOM **1 PASS / 16.71 с** (ChromeDriver 134.0.6998.165).
- Manual checklist: **PENDING HUMAN VERIFICATION** (`mobile/docs/kt09-manual-checklist.md`).
- Docs: `mobile/docs/kt09-cross-platform-*.md`, `docs/kt09/basic-cross-platform-matrix.md`.
- iOS: **NOT RUN**. Отчёт: `reports/KT09.docx`.

## КТ 08 — Скриншоты + Allure (compliance remediation 2026-10-10)

- **Оригинал презентации:** публичный сайт + Allure HTML со скриншотами (7 требований — PASS).
- Публичный сайт: https://www.saucedemo.com/ (the-internet.herokuapp.com заблокирован под Chrome automation).
- Public tests: `test_kt08_public_allure.py` (4); Pillow: `test_kt08_visual.py` (5, сохранены).
- Allure: allure-pytest **2.16.2**, CLI **2.37.0** → `selenium/artifacts/kt08/allure-report/`.
- Full suite: **9 passed in 34.64s**; исторический Pillow: **5 passed in 13.71s**.
- Отчёт обновлён: `reports/KT08.docx`.

## КТ 07 — Selenium Grid 4 (remediation 2026-10-10)

- JAR: `selenium-server-4.50.0` (SeleniumHQ release; вне Git).
- Исторический Standalone: **5 PASS / 4.88 с**; Hub+1 Node сохранён.
- Новое: Hub + Node A(:5556) + Node B(:5557); status **nodes=2**.
- Multi-browser: Chrome+Firefox **4 PASS / 7.72 с**; parallel overlap **true**.
- Скрипты: `start_hub_multi_node.ps1`, `scripts/run_kt07_multi.ps1`, `run_kt07_parallel_proof.py`.
- Документы: `docs/kt07/multi-node.md`; отчёт `reports/KT07.docx`.
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

## КТ 02 — Функциональные техники (remediation 2026-10-10)

- Исторический слой: windows/iframe **6 PASS / 21.49 с** (сохранён).
- Новое: публичный Sauce Demo **11 PASS / 49.34 с** (pos/neg/boundary/locators/cookies/windows).
- Код: `selenium/tests/test_kt02_sauce_public.py`, PO `selenium/pages/sauce/`.
- Скриншоты: `screenshots/kt02/public/`; docs: `docs/kt02/`; отчёт `reports/KT02.docx`.

## КТ 03 — Page Object (remediation 2026-10-10)

- Исторический локальный PO окон/iframe: **4 PASS / 14.90 с** (сохранён).
- Новое: публичный Sauce Demo PO **5 PASS / 21.11 с** (`test_kt03_sauce_po.py`).
- PO: `selenium/pages/sauce/`; скриншоты `screenshots/kt03/public/`; `reports/KT03.docx`.

## КТ 01

См. `reports/KT01.docx`.
