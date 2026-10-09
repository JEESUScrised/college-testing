# Selenium — КТ 01+

## КТ 01: открытие https://ya.ru в Chrome

### Требования окружения (Windows)

- Python 3.10+
- Google Chrome
- Интернет-доступ к `https://ya.ru`

Selenium 4 подтягивает совместимый ChromeDriver через Selenium Manager.

### Установка

Из корня репозитория:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r selenium\requirements.txt
```

### Запуск КТ 01

```powershell
.\.venv\Scripts\Activate.ps1
pytest selenium\tests\test_kt01_ya_ru.py -v --browser=chrome
```

Скриншот успешной навигации сохраняется в `screenshots/kt01/ya_ru_opened.png`.

## КТ 02: окна/вкладки и iframe

Публичный демо-сайт `https://the-internet.herokuapp.com` проверен (HTTP 200 для `/windows` и `/iframe`).
Для стабильных локаторов и воспроизводимости без зависимости от TinyMCE используются локальные HTML-фикстуры в `selenium/fixtures/kt02/`.

### Запуск КТ 02

```powershell
.\.venv\Scripts\Activate.ps1
pytest selenium\tests\test_kt02_windows.py selenium\tests\test_kt02_iframe.py -v --browser=chrome
```

Или по маркеру:

```powershell
pytest -m kt02 -v --browser=chrome
```

Скриншоты: `screenshots/kt02/`.

### Регрессия КТ 01 + КТ 02

```powershell
pytest selenium\tests -v --browser=chrome
```
