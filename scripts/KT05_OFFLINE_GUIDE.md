# KT05 — запуск без VPN (инструкция для Windows)

Цель: подготовить всё **при включённом VPN**, затем **один раз** прогнать Selenium-тесты KT05 на прямой сети (без VPN и без Cursor).

Сайт: `https://vdnh.ru/news/`  
Тесты: `selenium/tests/test_kt05_vdnh_news.py`

---

## 1. VPN включён — подготовка

Откройте PowerShell:

```powershell
cd C:\Users\admnp\Desktop\ITHUB\Testing\college-testing
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\prepare_kt05.ps1
```

Скрипт:

- проверит Python и `.venv`;
- установит зависимости из `selenium\requirements.txt`;
- найдёт Google Chrome;
- скачает совместимый ChromeDriver и положит в `selenium\drivers\chromedriver.exe`;
- выполнит `pytest --collect-only` для KT05 **без открытия сайта**.

Дождитесь сообщения **«Подготовка завершена»** и кода выхода `0`.

Если подготовка упала — не отключайте VPN, исправьте ошибку и повторите `prepare_kt05.ps1`.

---

## 2. VPN отключить вручную

Отключите VPN в вашей программе VPN.

Скрипты **не** меняют VPN и системные proxy.

---

## 3. Запуск KT05 в отдельном окне PowerShell

Важно: запуск **не из Cursor**, а из обычного PowerShell.

```powershell
cd C:\Users\admnp\Desktop\ITHUB\Testing\college-testing
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\run_kt05_no_vpn.ps1
```

Скрипт:

- использует только локальный `.venv` и `selenium\drivers\chromedriver.exe`;
- **не** скачивает пакеты и драйверы;
- запускает **ровно один** прогон KT05;
- открывает обычный (headed) Chrome;
- пишет лог, JUnit XML и HTML-отчёт;
- сохраняет скриншоты через существующие тесты.

Не запускайте скрипт повторно, пока не завершится текущий прогон.  
Автоповторов нет. Если остался `selenium\artifacts\kt05\run.lock` после сбоя — удалите его вручную.

---

## 4. Дождаться завершения

Дождитесь блока **«ИТОГ»** в консоли.

| Код выхода | Значение |
|---:|---|
| `0` | Все тесты KT05 в этом прогоне PASS |
| `1` | Есть FAIL (упавшие assertions) |
| `2+` | Ошибка запуска / прерывание / проблемы окружения |

---

## 5. VPN снова включить

Включите VPN.

---

## 6. Вернуться в Cursor и передать артефакты

Пришлите содержимое (или пути) к файлам:

- `selenium/artifacts/kt05/pytest_*.log`
- `selenium/artifacts/kt05/summary_*.txt`
- `selenium/artifacts/kt05/junit_*.xml`
- `selenium/artifacts/kt05/report_*.html`
- `screenshots/kt05/*.png`

По этим результатам можно будет обновить `docs/STATUS.md` и сформировать `reports/KT05.docx`.

---

## Целевой повтор только для FAIL (по необходимости)

Если исправлен Page Object для «Показать ещё», **не** гоняйте все 10 тестов снова. Один раз без VPN:

```powershell
cd C:\Users\admnp\Desktop\ITHUB\Testing\college-testing
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\run_kt05_show_more_only.ps1
```

Артефакты: `selenium/artifacts/kt05/pytest_show_more_*.log`, `summary_show_more_*.txt`.

---

## Где что лежит

| Что | Путь |
|---|---|
| Подготовка | `scripts/prepare_kt05.ps1` |
| Запуск | `scripts/run_kt05_no_vpn.ps1` |
| Локальный драйвер | `selenium/drivers/chromedriver.exe` |
| Логи/отчёты | `selenium/artifacts/kt05/` |
| Скриншоты | `screenshots/kt05/` |

---

## Замечания по сети

- Скорость ~5 Mbps через VPN делает `vdnh.ru` крайне медленным для Selenium — поэтому прогон делается **без VPN**.
- Если в системе заданы `HTTP_PROXY`/`HTTPS_PROXY`, скрипт запуска очищает их **только в своём процессе**.
- Системный VPN/proxy Windows скриптами не меняется.
