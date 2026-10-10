# Отчёт о тестировании КТ 06 — Appium / Android

Дата выполнения: **2026-10-09**. Документация расширена: **2026-10-10**.

## Статус

**DONE / PASS** — 7 UI-тестов на эмуляторе `Medium_Phone_API_36.1`.  
История: suite №1 имел 1 FAIL (TextFields scroll) → fix PO → suite №2 **7 PASS / 44.63 с**.

## Выбор приложения и ограничения

ApiDemos — официальный sample (воспроизводимость). Не production: платежи/auth **N/A**.  
План: `kt06-test-plan.md`. Дефекты: `kt06-defect-analysis.md` (багов приложения не подтверждено).

## Среда

| Параметр | Значение |
|---|---|
| Appium / driver | 3.8.0 / uiautomator2@8.7.0 |
| Python / pytest | 3.13.2 / 8.4.2 |
| AVD | Medium_Phone_API_36.1 (API 36), udid emulator-5554 |
| APK | ApiDemos v6.0.18 |

Подробности: `mobile/environment-report.md`.

## Типы тестирования (факт)

Functional — да. Usability — наблюдения по скриншотам/навигации. Performance — длительность suite как ориентир среды. Compatibility — только API 36 emulator. Negative — ограничено возможностями demo UI.

## Результаты suite №2 (финал)

| # | Тест | Result |
|---|---|---|
| 1–7 | см. kt06-test-cases.md | **PASS** |

```
============================= 7 passed in 44.63s ==============================
```

## Скриншоты / артефакты

`screenshots/kt06/01_*.png` … `08_textfields.png`; `mobile/artifacts/pytest_kt06_*`.

## Compliance matrix (кратко)

| Требование преподавателя | Статус |
|---|---|
| Выбор приложения + ограничения | PASS (документировано) |
| Характеристики платформы | PASS |
| Стратегия / типы тестирования | PASS |
| Сценарии + preconditions/steps/expected/actual | PASS |
| Исполнение | PASS (7/7) |
| Дефекты | PASS (нет confirmed app bugs; INC-06-01 = test) |
| Анализ + рекомендации | PASS |
| iOS / real device / payments | NOT RUN / N/A |
