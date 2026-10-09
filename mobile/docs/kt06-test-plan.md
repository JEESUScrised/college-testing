# План тестирования КТ 06 — мобильное приложение (Appium)

## Цель

Проверить возможность автоматизированного UI-тестирования Android-приложения с помощью Appium 3 и драйвера UiAutomator2 на учебном образце ApiDemos.

## Объект тестирования

| Параметр | Значение |
|---|---|
| Приложение | Appium ApiDemos |
| Источник | https://github.com/appium/android-apidemos (release v6.0.18) |
| Package | `io.appium.android.apis` |
| Main activity | `.ApiDemos` |
| APK | `mobile/apps/ApiDemos-debug.apk` |
| SHA-256 | `A9EECF37B26CD084855C530DB81C2BB1B91F4C1B095A04F47AA7C20E2791F686` |

## Среда

- ОС: Windows 10/11
- Appium Server: 3.x, `http://127.0.0.1:4723`
- Automation: UiAutomator2
- Клиент: Appium-Python-Client 4+/5+, pytest
- Устройство: один Android emulator **или** одно физическое устройство на весь suite

## Объём

Минимум 6 осмысленных UI-сценариев:

1. Запуск приложения и проверка главного списка.
2. Навигация по меню (App).
3. Переход на экран Alert Dialogs.
4. Взаимодействие с кнопкой/диалогом (List dialog).
5. Ввод текста и проверка значения (Text Entry dialog).
6. Возврат назад (системный Back).
7. (доп.) Views → TextFields — ввод в EditText.

## Подход

- Page Object (`mobile/pages/`)
- Явные ожидания (`WebDriverWait`), без deprecated TouchAction / desired_capabilities
- Одна Appium-сессия на модуль; между тестами сброс activity, без рестарта эмулятора
- Скриншоты: `screenshots/kt06/`
- Артефакты: `mobile/artifacts/`

## Критерии готовности к прогону

- `adb devices` показывает хотя бы одно `device`
- Appium отвечает на `/status`
- APK на месте и хеш совпадает

## Критерии приёмки отчёта

- Фактический прогон выполнен
- Результаты PASS/FAIL зафиксированы
- Скриншоты подлинные
- DOCX на русском (`reports/KT06.docx`) — **только после прогона**

## Риски

- Нет system image / AVD → выполнение выполнения
- Изменение UI ApiDemos между версиями → обновление локаторов
- Медленный cold start эмулятора → таймауты сессии

## Связь с KT09

План среды и зависимости переиспользуются для жестов/свайпов (KT09) без смены Appium/APK.
