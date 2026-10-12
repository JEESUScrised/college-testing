# Модульное тестирование веб-приложений — Контрольные точки №1–12

**Студент:** Прилепов Никита Алексеевич  
**Группа:** 4P1.23

Практические работы по автоматизации тестирования: веб, мобильные сценарии, учёт дефектов в Jira и проверка gRPC-сервиса. Отчёты лежат в `reports/`.

## Контрольные точки

| КТ | Содержание | Отчёт |
|---|---|---|
| KT01 | Основы Selenium WebDriver | [KT01.docx](reports/KT01.docx) |
| KT02 | Функциональное тестирование SauceDemo | [KT02.docx](reports/KT02.docx) |
| KT03 | Паттерн Page Object | [KT03.docx](reports/KT03.docx) |
| KT04 | Учёт дефектов в Jira | [KT04.docx](reports/KT04.docx) |
| KT05 | Функциональное тестирование раздела новостей ВДНХ | [KT05.docx](reports/KT05.docx) |
| KT06 | Мобильное тестирование Android (Appium) | [KT06.docx](reports/KT06.docx) |
| KT07 | Selenium Grid и параллельный запуск | [KT07.docx](reports/KT07.docx) |
| KT08 | Скриншотное тестирование, Pillow и Allure | [KT08.docx](reports/KT08.docx) |
| KT09 | Кроссплатформенное тестирование Windows и Android | [KT09.docx](reports/KT09.docx) |
| KT10 | Кроссбраузерное и адаптивное тестирование | [KT10.docx](reports/KT10.docx) |
| KT11 | Robot Framework | [KT11.docx](reports/KT11.docx) |
| KT12 | Тестирование gRPC-сервиса | [KT12.docx](reports/KT12.docx) |

## Инструменты

Python, pytest, Selenium 4, Appium, Android Emulator, Selenium Grid, Robot Framework, Pillow, Allure, gRPC, Jira.

## Результаты (кратко)

- **KT04** — в Jira заведены и закрыты дефекты [KAN-4](https://collegeqakt04.atlassian.net/browse/KAN-4), [KAN-5](https://collegeqakt04.atlassian.net/browse/KAN-5), [KAN-6](https://collegeqakt04.atlassian.net/browse/KAN-6); исправления проверены Selenium. На team-managed проекте native Components недоступны (HTTP 405), вместо них использованы labels — подробности в отчёте.
- **KT05** — последний полный прогон по новостям ВДНХ: **10 PASS**.
- **KT06** — последний полный прогон Appium / ApiDemos: **10 PASS** (эмулятор Android).
- **KT08** — полный suite скриншотов: **9 PASS**, отчёт Allure с вложениями.
- **KT09** — автоматические скриншоты Windows и Android по SauceDemo; Android Chrome DOM: **11 PASS**. Ручная верификация отдельно: **PENDING**.
- **KT11** — **10** тест-кейсов Robot Framework, все прошли.
- **KT12** — **10** тест-кейсов gRPC (unary, streaming, ошибки и deadline), все прошли.

## Структура репозитория

- [reports/](reports/) — отчёты DOCX по каждой КТ
- [selenium/](selenium/) — веб-автотесты (Selenium, Grid, визуальные проверки)
- [mobile/](mobile/) — Appium и Android-сценарии
- [robot/](robot/) — тесты Robot Framework
- [grpc/](grpc/) — учебный InventoryService и pytest для gRPC
- [bug-reports/](bug-reports/) — материалы по дефектам (КТ04)
- [docs/](docs/) — планы, статусы и сопроводительная документация
- [screenshots/](screenshots/) — скриншоты фактических прогонов

## Сдача

Готовые Word-отчёты: каталог [reports/](reports/) (`KT01.docx` … `KT12.docx`).

Единый архив сдачи: [submission/KT01-KT12_READY_FOR_SUBMISSION.zip](submission/KT01-KT12_READY_FOR_SUBMISSION.zip).

Статус и compliance: [docs/STATUS.md](docs/STATUS.md), [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md), [docs/compliance/FINAL_REQUIREMENTS_MATRIX.md](docs/compliance/FINAL_REQUIREMENTS_MATRIX.md), [docs/compliance/SCREENSHOT_VISUAL_AUDIT.md](docs/compliance/SCREENSHOT_VISUAL_AUDIT.md).
