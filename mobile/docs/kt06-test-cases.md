# Тест-кейсы КТ 06 (ApiDemos / Appium)

Автотесты: `mobile/tests/test_kt06_api_demos.py` (или эквивалент в `mobile/tests/`).  
Финальный прогон: **7 PASS / 44.63 с** (2026-10-09).

| ID | Описание | Preconditions | Steps | Input | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|---|---|---|
| TC-01 | Запуск | Emulator+Appium+APK | Открыть ApiDemos | — | Список App/Views | Список виден | **PASS** | `01_*.png` |
| TC-02 | Меню App | Home | Tap App | — | Виден Alert Dialogs | Виден | **PASS** | `02_*.png` |
| TC-03 | Alert Dialogs | App | Tap Alert Dialogs | — | Кнопка List dialog | Видна | **PASS** | `03_*.png` |
| TC-04 | List dialog | Alert Dialogs | Open list → select item | list item | Диалог открыт/закрыт | OK | **PASS** | `04_*.png` |
| TC-05 | Text Entry | Alert Dialogs | Open → type → OK | user/pass demo | Username сохранён в поле | Сохранён | **PASS** | `05_*.png` |
| TC-06 | Back | Alert Dialogs | Back×2 | — | App → Home | OK | **PASS** | `06_*.png` |
| TC-07 | TextFields | Home | Views→scroll→TextFields→type | sample text | EditText = input | = input | **PASS** | `08_textfields.png` |

## NOT APPLICABLE (вне scope ApiDemos)

| ID | Тема | Почему N/A |
|---|---|---|
| N/A-01 | Оплата / корзина | Нет в ApiDemos |
| N/A-02 | Регистрация / auth backend | Нет |
| N/A-03 | iOS parity | Не выполнялось (см. KT09) |

## Изоляция

Каждый тест: `mobile: startActivity` → `io.appium.android.apis/.ApiDemos`.
