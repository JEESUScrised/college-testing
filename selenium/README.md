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

## КТ 03: Page Object

Классы страниц: `selenium/pages/` (`BasePage`, `WindowsMainPage`/`WindowsSecondaryPage`, `IframePage`).
Тесты используют те же локальные HTML-фикстуры КТ 02.

```powershell
.\.venv\Scripts\Activate.ps1
pytest selenium\tests\test_kt03_page_object.py -v --browser=chrome
# или
pytest -m kt03 -v --browser=chrome
```

Скриншоты: `screenshots/kt03/`.

## КТ 05: функциональные тесты VDNH

Сайт: `https://vdnh.ru/news/`. Page Object: `selenium/pages/vdnh_pages.py`.  
Документация: `docs/kt05/`. Offline-запуск: `scripts/KT05_OFFLINE_GUIDE.md`.

```powershell
# полный suite (предпочтительно без VPN)
.\scripts\run_kt05_no_vpn.ps1
# только show_more после правки
.\scripts\run_kt05_show_more_only.ps1
```

Зачётный прогон 2026-10-09: **9 PASS / 1 FAIL** (`test_show_more_loads_additional_cards`).

## КТ 04: дефекты и баг-трекинг

Учебное приложение: `selenium/fixtures/kt04/` (Campus Portal Demo, seeded bugs).
Документация: `bug-reports/`.

```powershell
.\.venv\Scripts\Activate.ps1
pytest selenium\tests\test_kt04_defects.py -v --browser=chrome
```

Ожидаемо: 2 PASS + 3 FAIL (тесты проверяют корректное поведение против seeded-дефектов).
Скриншоты: `screenshots/kt04/`.
