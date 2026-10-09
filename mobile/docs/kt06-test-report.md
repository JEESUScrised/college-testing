# Отчёт о тестировании КТ 06 — Appium / Android

Дата выполнения: **2026-10-09** (новый ПК после миграции).

## Статус выполнения

**DONE / PASS** — UI-тесты Appium выполнены на реальном эмуляторе `Medium_Phone_API_36.1`.

Файл `reports/KT06.docx` создан по фактическим артефактам.

## Среда

Подробности: [`../environment-report.md`](../environment-report.md).

| Параметр | Значение |
|---|---|
| Appium | 3.8.0 (local `mobile/node_modules`) |
| Driver | uiautomator2@8.7.0 |
| Doctor | 0 required fixes |
| Node | v22.14.0 / npm 10.9.2 |
| Java | Android Studio JBR 21 |
| Python / pytest | 3.13.2 / 8.4.2 |
| SDK | `C:\Users\user\AppData\Local\Android\Sdk` |
| AVD | Medium_Phone_API_36.1 (API 36) |
| udid | emulator-5554 |
| APK | ApiDemos v6.0.18, SHA-256 проверен |

## Результаты

| # | Тест | Suite №1 | После фикса / Suite №2 |
|---|---|---|---|
| 1 | test_app_starts_and_shows_home | PASS | PASS |
| 2 | test_navigate_to_app_menu | PASS | PASS |
| 3 | test_open_alert_dialogs_screen | PASS | PASS |
| 4 | test_list_dialog_interaction | PASS | PASS |
| 5 | test_text_entry_dialog_input | PASS | PASS |
| 6 | test_back_returns_to_previous_screen | PASS | PASS |
| 7 | test_views_textfields_input | FAIL (scroll) | PASS |

Финал: **7 passed in 44.63s**.

## Исправление

На API 36 пункт `TextFields` вне видимой области списка Views.
Добавлен `BaseMobilePage.click_menu_item` с `UiScrollable.scrollIntoView`.

## Скриншоты

`screenshots/kt06/01_*.png` … `08_textfields.png` — подлинные PNG с сессии Appium.

## Артефакты

- `mobile/artifacts/pytest_kt06_20261009_211440.log`
- `mobile/artifacts/junit_kt06_20261009_211440.xml`
- `mobile/artifacts/report_kt06_20261009_211440.html`
- `mobile/artifacts/summary_20261009_211526.md`
