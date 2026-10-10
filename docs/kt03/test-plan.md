# KT03 — План (remediation: публичный Page Object)

## Цель

Применить паттерн Page Object к публичному сайту Sauce Demo, переиспользуя `selenium/pages/sauce/`. Исторический локальный PO (окна/iframe) сохраняется.

## Команда

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt03_sauce_po.py -v --browser=chrome --page-load-strategy=eager
```
