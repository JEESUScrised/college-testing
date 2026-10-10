# План тестирования — КТ 08 (оригинальные требования + Pillow)

## Цель (из презентации преподавателя)

Изучить скриншотное тестирование веб-приложений и интегрировать результаты с **Allure**.

## Два контура

| Контур | Назначение | Файл |
|---|---|---|
| A. Публичный сайт + Allure | Требование преподавателя | `test_kt08_public_allure.py` |
| B. Локальная Pillow regression | Доп. детерминированный контур | `test_kt08_visual.py` |

## Публичный сайт

**Выбран:** https://www.saucedemo.com/  
**Причина отказа от** https://the-internet.herokuapp.com/ — под Chrome automation страница отдаёт пустой DOM (challenge/bot protection); Sauce Demo стабильно открывается.

Сценарии: login page, inventory после login, sort dropdown, add to cart.

## Allure

- `allure-pytest` 2.16.2 → `selenium/artifacts/kt08/allure-results/`
- CLI Allure 2.37.0 → `selenium/artifacts/kt08/allure-report/`
- PNG через `allure.attach.file(..., AttachmentType.PNG)` в шагах тестов

## Команда

```powershell
.\scripts\run_kt08.ps1 -Mode Full
.\scripts\run_kt08.ps1 -Mode Public
.\scripts\run_kt08.ps1 -Mode Pillow
.\scripts\run_kt08.ps1 -Mode DiagnosticPublic
```
