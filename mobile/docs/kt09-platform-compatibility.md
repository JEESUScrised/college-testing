# Кроссплатформенная совместимость — КТ 09

## A. BASIC public web (Sauce Demo)

| OS | Browser | Method | Result |
|---|---|---|---|
| Windows 10 | Chrome / Firefox | Selenium Desktop | PASS (2) |
| Android 16 API 36 | Chrome 134.0.6998.135 | Appium + ChromeDriver 134.0.6998.165 DOM | **11 PASS / 36.91s** |
| iOS | Safari | — | **NOT RUN** |
| Manual Win/Android | — | Human checklist | **PENDING HUMAN VERIFICATION** |

Details: `kt09-platform-comparison.md`, `kt09-cross-platform-results.md`.

## B. Gestures (ApiDemos, supplementary)

- Жесты: `mobile: swipeGesture` / `scrollGesture` на Android — **5 PASS / 54.93s** (сохранены).
- iOS gesture port — NOT RUN (нет симулятора/XCUITest).

## Ограничение

Общий `GesturePort` ≠ успешный прогон на двух мобильных ОС. BASIC web Android DOM выполнен; ручная проверка человеком ещё не подтверждена.
