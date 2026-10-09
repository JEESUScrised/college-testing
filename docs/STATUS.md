# Статус контрольных точек

Дата начала: 2026-10-09.

| КТ | Статус | Тесты | Отчёт | Примечания |
|---|---|---|---|---|
| 01 | DONE | PASS | DONE | Selenium Chrome + ya.ru; регрессия при КТ 03: PASS; отчёт `reports/KT01.docx` |
| 02 | DONE | PASS | DONE | Окна/iframe; регрессия при КТ 03: 6 PASS; отчёт `reports/KT02.docx` |
| 03 | DONE | PASS | DONE | Page Object; `4 passed in 14.90s`; скриншоты `screenshots/kt03/`; отчёт `reports/KT03.docx` |
| 04 | TODO | NOT RUN | TODO | Баг-репорты / трекер |
| 05 | TODO | NOT RUN | TODO | Функциональные тесты |
| 06 | TODO | NOT RUN | TODO | Appium |
| 07 | TODO | NOT RUN | TODO | Grid |
| 08 | TODO | NOT RUN | TODO | Визуальное сравнение |
| 09 | TODO | NOT RUN | TODO | Свайпы |
| 10 | TODO | NOT RUN | TODO | Браузеры + отчеты |
| 11 | TODO | NOT RUN | TODO | 10 Robot тестов |
| 12 | TODO | NOT RUN | TODO | 10 gRPC тестов |

Значения: TODO — не начато, IN PROGRESS — в процессе, DONE — выполнено с реальными доказательствами, BLOCKED — есть препятствие. Тесты: PASS / FAIL / SKIP / NOT RUN.

## КТ 01 — факт прогона

- Среда: Windows 11 (10.0.26100), Python 3.13.9, Selenium 4.50.0, pytest 8.4.2, Google Chrome 154.0.8037.98.
- Команда: `pytest selenium\tests\test_kt01_ya_ru.py -v --browser=chrome`
- Результат: PASS (исторический прогон и регрессии).
- Доказательство: `screenshots/kt01/ya_ru_opened.png`
- Отчёт: `reports/KT01.docx`

## КТ 02 — факт прогона

- Команда: `pytest selenium\tests\test_kt02_windows.py selenium\tests\test_kt02_iframe.py -v --browser=chrome`
- Результат: `6 passed`; регрессия при КТ 03 подтверждена в общем прогоне 7 tests (KT01+KT02).
- Скриншоты: `screenshots/kt02/`
- Отчёт: `reports/KT02.docx`

## КТ 03 — факт прогона

- Среда: Windows 11, Python 3.13.9, Selenium 4.50.0, pytest 8.4.2, Chrome 154.0.8037.98.
- Классы: `selenium/pages/base_page.py`, `windows_page.py` (`WindowsPage`/`WindowsMainPage`, `WindowsSecondaryPage`), `iframe_page.py`.
- Команда: `pytest selenium\tests\test_kt03_page_object.py -v --browser=chrome`
- Результат: `4 passed in 14.90s`, warnings: нет, exit code: 0.
  - `test_po_open_secondary_window` PASS
  - `test_po_switch_and_verify_secondary_content` PASS
  - `test_po_close_secondary_and_return` PASS
  - `test_po_iframe_interact_and_return_to_default` PASS
- Регрессия КТ 01+02: `7 passed in 29.05s`, exit code: 0.
- Скриншоты: `screenshots/kt03/01_*.png` … `09_*.png`
- Отчёт: `reports/KT03.docx` (генератор `reports/build_kt03_docx.py`)
