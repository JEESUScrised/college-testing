# Статус контрольных точек

Дата начала: 2026-10-09.

| КТ | Статус | Тесты | Отчёт | Примечания |
|---|---|---|---|---|
| 01 | DONE | PASS | DONE | Selenium Chrome + ya.ru; регрессия 2026-10-09: `1 passed in 4.53s`; отчёт `reports/KT01.docx` |
| 02 | DONE | PASS | DONE | Окна/вкладки + iframe; `6 passed in 21.49s`; скриншоты `screenshots/kt02/`; отчёт `reports/KT02.docx` |
| 03 | TODO | NOT RUN | TODO | Page Object |
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
- Результат повторного прогона (после `pytest.ini`): `1 passed in 4.99s`, warnings: нет, exit code: 0.
- Регрессия при сдаче КТ 02 (2026-10-09): `1 passed in 4.53s`.
- Доказательство: `screenshots/kt01/ya_ru_opened.png`
- Отчёт: `reports/KT01.docx`

## КТ 02 — факт прогона

- Среда: та же (Windows 11, Python 3.13.9, Selenium 4.50.0, pytest 8.4.2, Chrome 154.0.8037.98).
- Публичный сайт `the-internet.herokuapp.com` проверен (HTTP 200 для `/windows` и `/iframe`); для стабильности использованы локальные HTML-фикстуры `selenium/fixtures/kt02/`.
- Команда: `pytest selenium\tests\test_kt02_windows.py selenium\tests\test_kt02_iframe.py -v --browser=chrome`
- Результат: `6 passed in 21.49s`, exit code: 0.
  - `test_open_new_browser_window` PASS
  - `test_switch_to_new_window_by_handle` PASS
  - `test_verify_new_window_content` PASS
  - `test_close_secondary_and_return_to_original` PASS
  - `test_switch_into_iframe_interact_and_verify` PASS
  - `test_return_to_default_content` PASS
- Скриншоты: `screenshots/kt02/01_*.png` … `10_*.png`
- Отчёт: `reports/KT02.docx` (генератор `reports/build_kt02_docx.py`)
