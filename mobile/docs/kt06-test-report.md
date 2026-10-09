# Отчёт о тестировании КТ 06 — Appium / Android

Дата подготовки проекта: **2026-10-09**.

## Статус выполнения

**BLOCKED / NOT RUN** — автоматизированные UI-тесты **не запускались** на реальном устройстве или эмуляторе.

Причина: в среде аудита отсутствуют:

- Android **system-images**;
- любые **AVD** (`emulator -list-avds` пуст);
- подключённые физические устройства (`adb devices` пуст).

Согласно требованиям задания: *не симулировать успешный прогон Appium* и *не создавать DOCX с заявлением о завершении*, если тесты не выполнялись.

Файл `reports/KT06.docx` **не создан**.

## Среда (по аудиту)

Подробности: [`../environment-report.md`](../environment-report.md).

| Параметр | Значение |
|---|---|
| Appium | 3.8.0 (local `mobile/node_modules`) |
| Driver | uiautomator2@8.7.0 |
| Doctor | 0 required fixes |
| Node | v25.0.0 / npm 11.6.2 |
| Java | Temurin 17.0.1 |
| Python / pytest | 3.13.9 / 8.4.2 |
| SDK | `C:\Users\admnp\AppData\Local\Android\Sdk` |
| APK | ApiDemos v6.0.18, SHA-256 проверен |
| Устройство | **нет** |

## Подготовленные тест-кейсы

Реализованы в коде (7 штук), см. `kt06-test-cases.md`. Фактические PASS/FAIL — **нет данных** (прогон не выполнялся).

## Скриншоты

Каталог `screenshots/kt06/` подготовлен скриптом прогона. Подлинных скриншотов **нет** (нет сессии Appium).

## Артефакты

После снятия блокировки ожидаются:

- `mobile/artifacts/pytest_kt06_*.log`
- `mobile/artifacts/junit_kt06_*.xml`
- `mobile/artifacts/report_kt06_*.html`

## Как повторить прогон после появления устройства

```powershell
.\scripts\diagnose_kt06.ps1
.\scripts\start_kt06_services.ps1
.\scripts\run_kt06.ps1
.\scripts\collect_kt06_artifacts.ps1
```

Затем обновить этот файл фактическими результатами и сгенерировать `reports/KT06.docx`.

## Вывод

Каркас KT06 (зависимости, Page Object, тесты, скрипты, документация) **готов**.  
Исполнение и отчёт DOCX — **заблокированы** отсутствием Android runtime (AVD/device).
