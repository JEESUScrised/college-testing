# Отчёт о тестировании — КТ 07

Дата: **2026-10-09**.

## Среда

| Параметр | Значение |
|---|---|
| OS | Windows 10.0.19045 x64 |
| Java | Android Studio JBR 21 |
| Python / Selenium | 3.13.2 / 4.50.0 |
| Chrome | 155.0.8059.39 |
| Grid | selenium-server **4.50.0** |
| Bind | `127.0.0.1` (не публичный интернет) |

## Прогоны

### Диагностика (Standalone)

`test_remote_session_created` — **PASS** (~0.74 с).

### Suite Standalone (полный)

**5 passed in 4.88s**, exit 0.  
Артефакты: `selenium/artifacts/kt07/pytest_kt07_20261009_213132.log`, `junit_…`, `report_…`.

### Hub + Node

- Node `uri=http://127.0.0.1:5556` зарегистрирован, `ready=true`, nodes=1.
- Проверка сессий: `test_remote_session_created` + `test_navigate_and_title` — **2 PASS** (~1.96 с).
- Event Bus: `tcp://127.0.0.1:4442/4443` (обход VPN-IP 26.x).

## Результаты suite (Standalone)

| ID | Тест | Результат |
|---|---|---|
| TC-07-01 | test_remote_session_created | PASS |
| TC-07-02 | test_navigate_and_title | PASS |
| TC-07-03 | test_dom_element_interaction | PASS |
| TC-07-04 | test_window_open_and_switch | PASS |
| TC-07-05 | test_iframe_interaction_and_context_switch | PASS |

## Скриншоты

`screenshots/kt07/01_*.png` … `09_iframe_default_content.png`.

## Ограничение

Hub + Node на **одной** машине подтверждает протокол Grid (регистрация Node, маршрутизация сессий). Отдельные физические машины **не** тестировались.
