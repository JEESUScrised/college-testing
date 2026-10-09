# План тестирования — КТ 08

## Цель

Реализовать воспроизводимый screenshot visual regression: захват реальных скриншотов Selenium Chrome, сравнение с approved baseline через Pillow, детекция осмысленных отличий и генерация диагностических артефактов.

## Источник требований

Презентация https://cloud.ithub.ru/index.php/s/mxkfJ97fjj9e6yT недоступна без авторизации (виден только заголовок). План опирается на формулировку задания в репозитории/чате; полное соответствие скрытым слайдам **не утверждается**.

## Объект

Локальные HTML-фикстуры `selenium/fixtures/kt08/` (детерминированный layout, без внешних сайтов).

## Среда

Windows 10; Python 3.13; Selenium 4; Pillow 11; Chrome; viewport window 1400×1000.

## Сценарии

1. Match с baseline  
2. Детекция text/color change  
3. Детекция layout shift  
4. Significant difference + метрики  
5. Dimension mismatch без resize  

## Критерии

- Match: `diff_percent <= 0.75%` при tolerance=12  
- Ожидаемые отличия: тест PASS только если утилита **обнаружила** отличие  
- Baseline не обновляется автоматически  
