# КТ 11 — План тестирования (Robot Framework)

## Цель

Реализовать **ровно 10** различимых автотестов на Robot Framework + SeleniumLibrary с keyword-driven подходом, локальным HTML-приложением и стандартными отчётами Robot (`output.xml`, `log.html`, `report.html`).

## Объект тестирования

Локальное приложение `robot/fixtures/`:

| Страница | Назначение |
|---|---|
| `index.html` | Home, навигация, динамический статус, ссылка на новую вкладку |
| `register.html` | Форма регистрации (валид / невалид) |
| `controls.html` | Checkbox, radio, dropdown |
| `frames.html` + `frame_inner.html` | iframe |
| `secondary.html` | Вторичная вкладка |

HTTP: `FixtureServer` (динамический порт `127.0.0.1`).

## Стратегия

- Native `.robot` синтаксис; Python только для HTTP-сервера.
- Chrome (матрица Firefox не требуется для КТ11).
- Suite Setup/Teardown: сервер + закрытие браузеров.
- Test Teardown: `Close Browser` (независимые сессии).
- Явные ожидания SeleniumLibrary; без `Sleep`.
- Screenshot-on-failure через `run_on_failure=Capture Page Screenshot`.

## Критерий приёмки

10/10 PASS; артефакты в `robot/artifacts/kt11/`; скриншоты в `screenshots/kt11/`; отчёт `reports/KT11.docx`.
