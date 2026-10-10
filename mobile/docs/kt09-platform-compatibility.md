# Кроссплатформенная совместимость — КТ 09

## Что сделано на Android

- Жесты: `mobile: swipeGesture`, `mobile: scrollGesture`, опционально W3C Pointer Actions.  
- Координаты из размеров окна/элемента с отступом от системных краёв.  
- Реальные экраны ApiDemos (Views list, Gallery).

## Как адаптировать для iOS (не выполнялось)

| Слой | Android (факт) | iOS (план) |
|---|---|---|
| Driver | UiAutomator2 | XCUITest |
| Gesture API | `mobile: swipeGesture` / `scrollGesture` | `mobile: swipe` / `mobile: scroll` (XCUITest) или W3C actions |
| Port | `AndroidGesturePort` | реализовать `IOSGesturePort` |
| Локаторы | accessibility id / resource-id | accessibility id / iOS predicate |
| Приложение | ApiDemos APK | аналог demo app / XCUITest sample |

Общий тест-код должен вызывать только `GesturePort` и Page Object с платформенными локаторами.

## Ограничение

**iOS не тестировался.** Нет симулятора/устройства, нет XCUITest-драйвера, нет iOS-сборки.  
Наличие общего `GesturePort` **не** означает успешное кроссплатформенное выполнение.
