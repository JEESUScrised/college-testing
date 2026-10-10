# План тестирования — КТ 09 (жесты / кроссплатформенность)

## Цель

Продемонстрировать реальные swipe/scroll-взаимодействия Appium на Android с assertions, подтверждающими изменение UI. Заложить кроссплатформенную структуру намерений без фиктивного прогона iOS.

## Источник требований

Презентация https://cloud.ithub.ru/index.php/s/58xH5Pa4RP65BK5 недоступна без авторизации (виден заголовок). План опирается на формулировку задания; соответствие скрытым слайдам **не утверждается**.

## Среда

- Windows 10; Appium 3.8.0; UiAutomator2 8.7.0; Python 3.13  
- AVD `Medium_Phone_API_36.1` (API 36)  
- ApiDemos v6.0.18  
- iOS / XCUITest: **не выполнялось**

## Объект

Экраны ApiDemos: `Views` (вертикальный список), `Views/Gallery/1. Photos` (горизонтальный `Gallery`).

## Подход

1. Высокоуровневый контракт `GesturePort` (platform-agnostic).  
2. Исполнение `AndroidGestures` (`mobile: swipeGesture` / `scrollGesture`, W3C fallback).  
3. iOS-порт — заглушка `NotImplementedError` (документировано).
