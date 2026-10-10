# KT12 — План тестирования gRPC

## Цель

Проверить реальный локальный InventoryService через HTTP/2 gRPC: unary, streaming, ошибки статусов и deadline.

## Объект

In-memory InventoryService на `127.0.0.1` со свободным портом (OS-assigned). Внешние БД не используются.

## Стратегия

- pytest + сгенерированные stubs;
- фикстура поднимает сервер / канал / stub на каждый тест (изолированное состояние);
- без моков и прямых вызовов методов сервиса вместо RPC;
- артефакты: JUnit, HTML, evidence.jsonl, versions.json.

## Критерий

10/10 PASS; `reports/KT12.docx`; STATUS обновлён для всех 12 КТ.
