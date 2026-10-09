# Статус контрольных точек

Дата начала: 2026-10-09.

| КТ | Статус | Тесты | Отчёт | Примечания |
|---|---|---|---|---|
| 01 | DONE | PASS | DONE | Selenium Chrome + ya.ru; повторный прогон после `pytest.ini`: `1 passed in 4.99s`, без warnings; скриншот `screenshots/kt01/ya_ru_opened.png`; отчёт `reports/KT01.docx` |
| 02 | TODO | NOT RUN | TODO | Окна и iframe |
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
- Доказательство: `screenshots/kt01/ya_ru_opened.png`
- Отчёт: `reports/KT01.docx` (скриншот встроен, проверен через python-docx).
- Генератор отчёта: `reports/build_kt01_docx.py`
