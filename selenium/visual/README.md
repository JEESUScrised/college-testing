# Visual regression (KT08) — Selenium + Pillow

## Что делает модуль

`visual/compare.py` сравнивает утверждённый baseline PNG с актуальным скриншотом Selenium:

- загрузка и валидация изображений;
- отказ при несовпадении размеров (**без auto-resize**);
- per-pixel сравнение с допуском цвета (`color_tolerance`);
- процент изменённых пикселей;
- diff-mask и overlay с подсветкой;
- диагностическое сообщение с метриками.

Базовые изображения **не перезаписываются** при FAIL.

## Генерация baseline

```powershell
.\.venv\Scripts\python.exe selenium\visual\generate_kt08_baselines.py
```

Результат: `selenium/baselines/kt08/home_baseline.png` + `baseline_manifest.json`.

## Запуск тестов

```powershell
.\scripts\run_kt08.ps1
```

Артефакты: `screenshots/kt08/`, `selenium/artifacts/kt08/` (masks, overlays, summary JSONL).

## Параметры по умолчанию в тестах

| Параметр | Значение |
|---|---|
| window size | 1400×1000 |
| color_tolerance | 12 |
| match threshold | 0.75% changed pixels |

## Ограничения

- Чувствительно к DPI/шрифтам/версии Chrome.
- Не заменяет semantic UI-тесты.
- Презентация KT08 на cloud.ithub.ru недоступна без авторизации — требования взяты из формулировки задания в чате.
