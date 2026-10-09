# Тест-кейсы КТ 06 (ApiDemos / Appium)

Локаторы взяты из реального UI ApiDemos (accessibility id / resource-id). Выдуманные экраны не используются.

| ID | Название | Предусловия | Шаги | Ожидаемый результат | Автотест |
|---|---|---|---|---|---|
| TC-01 | Запуск приложения | Устройство готово, APK установлен Appium | Открыть ApiDemos | Виден список с пунктами App, Views | `test_app_starts_and_shows_home` |
| TC-02 | Навигация в App | На домашнем экране | Нажать App | Виден пункт Alert Dialogs | `test_navigate_to_app_menu` |
| TC-03 | Экран Alert Dialogs | — | App → Alert Dialogs | Видна кнопка List dialog | `test_open_alert_dialogs_screen` |
| TC-04 | List dialog | На Alert Dialogs | Нажать List dialog → выбрать пункт списка | Диалог открывается (заголовок), затем закрывается | `test_list_dialog_interaction` |
| TC-05 | Text Entry dialog | На Alert Dialogs | Открыть Text Entry dialog → ввести username/password → OK | Поле username содержит введённое значение | `test_text_entry_dialog_input` |
| TC-06 | Кнопка Back | Alert Dialogs открыт | Нажать Back дважды | Возврат на App, затем на Home | `test_back_returns_to_previous_screen` |
| TC-07 | TextFields | Home | Views → TextFields → ввод в EditText | Текст в поле совпадает с введённым | `test_views_textfields_input` |

## Изоляция

Каждый тест начинается с `mobile: startActivity` → `io.appium.android.apis/.ApiDemos`.
