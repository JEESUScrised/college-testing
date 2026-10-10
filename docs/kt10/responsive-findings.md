# KT10 — Responsive findings

Дата: 2026-10-10.

## Наблюдения

- **Горизонтальный overflow:** не зафиксирован ни в одном из 36 кейсов (`horizontal_overflow=false`).
- Login / inventory / burger menu / cart / checkout fields доступны на desktop, tablet и phone (Chrome CDP + Firefox resize).
- Chrome: нативная HTML5 `required` блокировала показ баннера Sauce без JS-click на Continue — учтено в Page Object.
- Firefox resize ≠ эмулятор Android/iOS (явно в отчёте).

## Рекомендации

1. Для мобильных сценариев дополнительно проверять на реальном Android Chrome (см. KT09).
2. Фиксировать `innerWidth/innerHeight` из JS, не только outer window size.
3. Сохранять matrix JSONL для сравнения регрессий раскладки.
