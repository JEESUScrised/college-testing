# Тест-кейсы КТ 06 (ApiDemos / Appium)

Автотесты: `mobile/tests/test_kt06_appium.py`  
Исторический финал (2026-10-09): **7 PASS / 44.63 с**  
Remediation (2026-10-11): **10 PASS / 67.70 с** (сохраняет 7 базовых + 3 расширения)

| ID | Описание | Preconditions | Steps | Input | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|---|---|---|
| TC-01 | Запуск | Emulator+Appium+APK | Открыть ApiDemos | — | Список App/Views | Список виден | **PASS** | `01_*.png` |
| TC-02 | Меню App | Home | Tap App | — | Виден Alert Dialogs | Виден | **PASS** | `02_*.png` |
| TC-03 | Alert Dialogs | App | Tap Alert Dialogs | — | Кнопка List dialog | Видна | **PASS** | `03_*.png` |
| TC-04 | List dialog | Alert Dialogs | Open list → select item | list item | Диалог открыт/закрыт | OK | **PASS** | `04_*.png` |
| TC-05 | Text Entry | Alert Dialogs | Open → type → OK | user/pass demo | Username в поле | Сохранён | **PASS** | `05_*.png` |
| TC-06 | Back | Alert Dialogs | Back×2 | — | App → Home | OK | **PASS** | `06_*.png`, `07_*.png` |
| TC-07 | TextFields | Home | Views→TextFields→type | sample text | EditText = input | = input | **PASS** | `08_textfields.png` |
| TC-08 | Dialog Cancel | Alert Dialogs | Open Text Entry → fill → Cancel | cancel_user | Диалог закрыт, кнопка видна | Закрыт | **PASS** | `09_*.png`, `10_*.png` |
| TC-09 | Clear field | TextFields | type → clear | temporary | Ввод удалён; hint допустим | hint text | **PASS** | `11_textfields_cleared.png` |
| TC-10 | A11y labels | Home | Проверить content-desc App/Views | — | Labels доступны | OK | **PASS** | `12_home_a11y.png` |

## NOT APPLICABLE (вне scope ApiDemos)

| ID | Тема | Почему N/A |
|---|---|---|
| N/A-01 | Оплата / корзина | Нет в ApiDemos |
| N/A-02 | Регистрация / auth backend | Нет |
| N/A-03 | iOS parity | Не выполнялось (см. KT09) |
| N/A-04 | Orientation stress | Не добавлялось (нестабильно на emulator без отдельного scope) |

## Изоляция

Каждый тест: `mobile: startActivity` → `io.appium.android.apis/.ApiDemos`.

## Наблюдение по TC-09

После `clear()` UiAutomator возвращает текст hint (`hint text`) — ожидаемое поведение Android EditText, **не** дефект ApiDemos.
