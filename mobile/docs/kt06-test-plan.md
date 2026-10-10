# План тестирования КТ 06 — мобильное приложение (Appium)

## 1. Цель

Проверить UI-функциональность Android-приложения с помощью Appium 3 / UiAutomator2,
оформить стратегию, сценарии, результаты и анализ качества по требованиям преподавателя.

## 2. Выбор приложения

| Параметр | Значение |
|---|---|
| Приложение | **Appium ApiDemos** (официальный sample) |
| Источник | https://github.com/appium/android-apidemos (v6.0.18) |
| Package / Activity | `io.appium.android.apis` / `.ApiDemos` |
| APK | `mobile/apps/ApiDemos-debug.apk` |
| SHA-256 | `A9EECF37…F686` |

### Почему ApiDemos (и ограничения)

**Плюсы:** публичный sample; воспроизводимость; стабильные accessibility id; детерминированные
экраны (App, Alert Dialogs, Views/TextFields); подходит для обучения Appium без коммерческих рисков.

**Ограничения (честно):** это **не** production-приложение. Нет реальных платежей, бизнес-аккаунтов,
онлайн-синхронизации, push-уведомлений продукта. Сценарии «оплата / регистрация пользователя»
помечены **NOT APPLICABLE** к выбранному объекту.

Преподаватель предпочитает beta/low-rating apps, но не делает это абсолютным требованием.
ApiDemos выбран ради воспроизводимости учебного стенда на Windows + эмуляторе.

## 3. Характеристики платформы (факт)

| Аспект | Значение / наблюдение |
|---|---|
| OS / API | Android 16 / **API 36** (`Medium_Phone_API_36.1`) |
| Устройство | Emulator `emulator-5554` (не физическое) |
| Automation | UiAutomator2 8.7.0 + Appium 3.8.0 |
| Селекторы | accessibility id, resource-id, UiScrollable |
| Навигация | системный Back; списки меню ApiDemos |
| Клавиатура | soft keyboard на Text Entry / TextFields |
| Permissions | autoGrantPermissions в capabilities |
| Производительность эмулятора | cold start медленнее реального устройства; AEHD acceleration |
| Эмулятор vs device | жесты/тайминги и DPI могут отличаться на реальном телефоне |

## 4. Типы тестирования

| Тип | Что делали | Что не делали |
|---|---|---|
| **Functional** | Launch, меню App, Alert Dialogs, List/Text Entry dialogs, Back, TextFields | Платежи / auth (N/A) |
| **Usability** | Наблюдения по читаемости списков, доступности диалогов (авто + скриншоты) | Отдельная ручная UX-сессия с респондентами |
| **Performance** | Длительность suite (исторически 44.63 с / 7 TC; remediation 67.70 с / 10 TC) | SLA/нагрузочные метрики продукта |
| **Compatibility** | Android API 36 emulator | Другие API / iOS / физические устройства |
| **Negative / dismiss** | Cancel Text Entry; clear TextFields (hint остаётся) | Выдуманные кейсы без UI |
| **Accessibility** | content-desc пунктов App/Views на Home | Полный a11y audit / TalkBack |

## 5. Объём сценариев

1. Запуск и главный список.  
2. Навигация App.  
3. Alert Dialogs.  
4. List dialog.  
5. Text Entry dialog (ввод).  
6. Back navigation.  
7. Views → TextFields (ввод).  
8. Text Entry Cancel (dismiss).  
9. TextFields clear / empty (hint).  
10. Accessibility labels Home.

## 6. Критерии входа / выхода

**Вход:** `adb devices` = device; Appium `/status` ready; APK + хеш; AVD запущен.

**Выход:** ≥6 UI-тестов с фактом; скриншоты; docs; DOCX; PASS/FAIL без фальсификации.
Исторический 7/7 сохранён; remediation 10/10 (2026-10-11).

## 7. Архитектура

- Page Object: `mobile/pages/`
- Фикстуры: `mobile/conftest.py` (одна сессия на модуль)
- Скриншоты: `screenshots/kt06/`
- Связь с KT09: та же Appium/AVD среда

## 8. Риски

- TextFields вне экрана на API 36 → нужен scrollIntoView (исправлено).
- Нет второго API/device → совместимость ограничена.
- Demo-приложение ≠ оценка качества коммерческого продукта.
