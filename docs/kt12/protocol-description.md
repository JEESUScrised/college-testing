# KT12 — Описание протокола InventoryService

## Сообщения (Protocol Buffers)

Сообщения — сериализуемые структуры данных (`Item`, `CreateItemRequest`, …).  
Они не выполняют сеть; это контракт полей.

## Service definition

`service InventoryService` в `grpc/proto/inventory.proto` объявляет RPC-методы и типы потоков (unary / stream).

## Generated stubs

`grpc_tools.protoc` создаёт:

- `inventory_pb2.py` — классы сообщений;
- `inventory_pb2_grpc.py` — `InventoryServiceStub` (клиент) и `InventoryServiceServicer` (база сервера).

Файлы помечены `DO NOT EDIT` и генерируются скриптом `scripts/generate_kt12_proto.ps1`.

## Server implementation

`grpc/server/service.py` наследует `InventoryServiceServicer` и реализует бизнес-логику + `context.abort(StatusCode, …)`.

## Channels

Клиент открывает `grpc.insecure_channel("127.0.0.1:<port>")` (учебный loopback без TLS).  
Stub вызывает RPC через канал по HTTP/2.

## Status codes

| Код | Когда |
|---|---|
| OK | успешный RPC |
| ALREADY_EXISTS | дубликат id |
| INVALID_ARGUMENT | пустое имя / отрицательное quantity |
| NOT_FOUND | неизвестный id |
| DEADLINE_EXCEEDED | клиентский timeout < server delay (`SlowPing`) |
