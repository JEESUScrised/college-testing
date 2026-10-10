# Отчёт о тестировании КТ 06 — Appium / Android

Дата исходного исполнения: **2026-10-09**.  
Расширение suite и документации: **2026-10-11**.

## Статус

**DONE / PASS**

| Suite | Collected | Passed | Duration | Примечание |
|---|---|---|---|---|
| Исторический финал (2026-10-09) | 7 | **7** | 44.63 s | После fix scroll TextFields |
| Remediation (2026-10-11) | 10 | **10** | **67.70 s** | + Cancel, clear/hint, a11y |

## Выбор приложения и ограничения

ApiDemos — официальный sample (воспроизводимость). Не production: платежи/auth **N/A**.  
План: `kt06-test-plan.md`. Дефекты: `kt06-defect-analysis.md` (багов приложения не подтверждено).

## Среда

| Параметр | Значение |
|---|---|
| Appium / driver | 3.8.0 / uiautomator2 |
| Python / pytest | 3.13.2 / 8.4.2 |
| AVD | Medium_Phone_API_36.1 (API 36 / Android 16), udid `emulator-5554` |
| APK | ApiDemos (`io.appium.android.apis`) |

## Типы тестирования (факт)

| Тип | Применение |
|---|---|
| Functional | Навигация, диалоги, TextFields |
| Negative / dismiss | Cancel диалога; clear поля |
| Accessibility | content-desc пунктов Home |
| Usability | Наблюдения по скриншотам |
| Performance | Длительность suite как ориентир среды (~68 с / 10 тестов) |
| Compatibility | Только emulator API 36 |

## Результаты remediation suite

```
======================== 10 passed in 67.70s (0:01:07) ========================
```

Артефакты: `mobile/artifacts/kt06/junit_20261011_full.xml`, `report_20261011_full.html`.

## Скриншоты

`screenshots/kt06/01_*.png` … `12_home_a11y.png`.

## Defect summary

Подтверждённых дефектов приложения **нет**.  
INC-06-01 (исторический FAIL TextFields) = ошибка теста (scroll), исправлена.

## Compliance matrix

| Требование преподавателя | Статус |
|---|---|
| Выбор приложения + ограничения | PASS |
| Характеристики платформы Android 16 / emulator | PASS |
| Стратегия / типы тестирования | PASS |
| Сценарии + preconditions/steps/expected/actual | PASS (10 TC) |
| Исполнение | PASS (10/10 remediation; 7/7 historical preserved) |
| Дефекты | PASS (нет confirmed app bugs) |
| Анализ + рекомендации | PASS |
| iOS / real device / payments | NOT RUN / N/A |
