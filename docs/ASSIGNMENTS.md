# Реестр контрольных точек

Источники: формулировки, переданные студентом в чате; ссылки на презентации преподавателя.
Эта таблица — план, а не подмена оригинальных условий. Там, где текст задания не детализирован, требуется сверить презентацию.

| КТ | Баллы | Основное требование | Каталог |
|---|---:|---|---|
| 01 | 5 | Selenium Chrome открывает https://ya.ru | selenium/ |
| 02 | 10 | Тестирование функций сайта; переключение окон/iframe | selenium/ |
| 03 | неизвестно | Паттерн Page Object: страницы, локаторы, методы | selenium/pages/ |
| 04 | 5 | Документы дефектов и баг-трекер Jira либо аналог | bug-reports/ |
| 05 | 15 | Функциональные тесты сайта + тестовая документация | selenium/ + docs/ |
| 06 | 5 | Appium: мобильное приложение, тесты и документация | mobile/ |
| 07 | 15 | Удаленный запуск через Selenium Grid | selenium/grid/ |
| 08 | 5 | Скриншоты Selenium и сравнение Pillow | selenium/ |
| 09 | 5 | Кроссплатформенность и тестирование свайпов Appium | mobile/ |
| 10 | 10 | Кроссбраузерность, отчеты / listeners | selenium/ |
| 11 | 5 | Написать 10 тест-кейсов в Robot Framework | robot/ |
| 12 | 15 | Написать 10 тест-кейсов для gRPC | grpc/ |

Известная сумма: **95 баллов + КТ03** (баллы не указаны).

## Презентации
- КТ02: https://cloud.ithub.ru/index.php/s/ckbgP5GTm4ZGYsc
- КТ03: https://cloud.ithub.ru/index.php/s/i6zfcK8GWngEdEE
- КТ04: https://cloud.ithub.ru/index.php/s/NggXF5CFTYeHD7C
- КТ05: https://cloud.ithub.ru/index.php/s/zNNkZYBc6TFH5qz
- КТ06: https://cloud.ithub.ru/index.php/s/9Q6F95SHwJB3sJ2
- КТ07: https://cloud.ithub.ru/index.php/s/6qpHeM4xQgXjH3e
- КТ08: https://cloud.ithub.ru/index.php/s/mxkfJ97fjj9e6yT
- КТ09: https://cloud.ithub.ru/index.php/s/58xH5Pa4RP65BK5
- КТ10: https://cloud.ithub.ru/index.php/s/xMGTDmqxwiQQ8Pp

Пример преподавателя для КТ05: https://github.com/sa-teach/selenium-tests/tree/main

## Оговорки
- В КТ02, 04–10 указано «Выполнить задание из презентации» или «Задание» без полного текста, поэтому детали нельзя считать полностью выясненными.
- КТ09: материал объясняет свайпы, хотя заголовок — кроссплатформенное тестирование.
- КТ10: материал объясняет отчёты/listeners, хотя заголовок — кроссбраузерное тестирование.
- Старые примеры Selenium/Grid/Appium требуют адаптации для актуальных библиотек.
- Для КТ06 и КТ09 необходимо реальное Android-устройство или эмулятор; для КТ07 — работающий Grid и доступные браузеры.
