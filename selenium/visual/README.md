# Visual / screenshot testing (KT08)

## Два контура

1. **Публичный сайт + Allure** (требование презентации преподавателя)  
   `selenium/tests/test_kt08_public_allure.py` → https://www.saucedemo.com/
2. **Локальная Pillow visual regression** (доп. детерминированный контур)  
   `selenium/tests/test_kt08_visual.py` + `visual/compare.py`

## Allure

Зависимость: `allure-pytest` (см. `selenium/requirements.txt`).  
CLI: `allure` 2.37.0 (уже установлен: `C:\allure\allure-2.37.0\`).

```powershell
.\scripts\run_kt08.ps1 -Mode Full
# allure-results + allure-report под selenium/artifacts/kt08/
```

PNG крепятся через `allure.attach.file(..., AttachmentType.PNG)` (`visual/allure_helpers.py`).

## Pillow compare

`visual/compare.py` — baseline vs actual, без auto-resize, mask/overlay.

```powershell
.\.venv\Scripts\python.exe selenium\visual\generate_kt08_baselines.py
.\scripts\run_kt08.ps1 -Mode Pillow
```

Исторический результат Pillow: **5 passed in 13.71s**.

## Почему не the-internet.herokuapp.com

Под Chrome automation сайт отдаёт пустой DOM (challenge script). Sauce Demo выбран как доступный публичный demo с login/inventory/controls.
