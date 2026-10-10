# KT02 — План (remediation: публичный сайт)

## Цель

Дополнить исторические локальные сценарии окон/iframe публичным функциональным тестированием Sauce Demo с техниками: positive, negative, boundary, локаторы, cookies, window handles.

## Объект

https://www.saucedemo.com/ (`standard_user` / `secret_sauce`)

## Среда

- Windows, Python 3.13, pytest, Selenium 4, Chrome
- Page Object: `selenium/pages/sauce/`
- Маркер: `@pytest.mark.kt02_public`

## Команда

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt02_sauce_public.py -v --browser=chrome --page-load-strategy=eager
```

## Исторический слой (сохранён)

```powershell
pytest selenium\tests\test_kt02_windows.py selenium\tests\test_kt02_iframe.py -v --browser=chrome
```
