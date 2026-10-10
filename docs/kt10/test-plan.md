# KT10 — План (responsive remediation)

## Цель (оригинал презентации)

Кроссбраузерное тестирование **адаптивного** публичного веб-приложения: разные браузеры + эмуляция/resize desktop/tablet/smartphone, проверка меню/форм/раскладки, фиксация проблем, отчёт.

## Контуры

1. **Исторический** functional Chrome×Firefox 5×2 (локальные фикстуры) — `test_kt10_matrix.py` — **10 PASS / 52.92 с** (сохранить).
2. **Новый** responsive Sauce Demo — `test_kt10_responsive.py` — 6 профилей × TC10-R01…R06.

## Матрица

| Browser | Profile | Target | Mode |
|---|---|---|---|
| Chrome | desktop | 1440×900 | window resize |
| Chrome | tablet | 768×1024 | CDP deviceMetrics |
| Chrome | phone | 390×844 | CDP deviceMetrics |
| Firefox | desktop/tablet/phone | same | window resize (не Android/iOS) |

Сайт: https://www.saucedemo.com/
