# KT12 — Automated Testing of a Real gRPC Service

Локальный **InventoryService** (proto3) + ровно **10** pytest-тестов через реальные gRPC stubs / HTTP/2.

## Важно про импорты

Каталог проекта называется `grpc/`, но **не** содержит `__init__.py` на верхнем уровне — иначе он перекрыл бы пакет `grpcio`.  
Сгенерированные модули добавляются в `sys.path` из `conftest.py` (`grpc/generated`).

## Версии

| Пакет | Версия |
|---|---|
| grpcio / grpcio-tools | 1.84.0 |
| protobuf | 7.36.2 |
| pytest | 8.4.2 |

```powershell
.\.venv\Scripts\pip.exe install -r grpc\requirements.txt
.\scripts\generate_kt12_proto.ps1
```

## Структура

```
grpc/
  proto/inventory.proto
  generated/          # protoc output (inventory_pb2*.py)
  server/             # InventoryServicer + in-memory store
  client/cli.py       # демо CreateItem/GetItem
  tests/test_kt12_grpc.py
  conftest.py
  artifacts/kt12/
```

## RPC

| Метод | Тип |
|---|---|
| CreateItem / GetItem / UpdateStock / SlowPing | unary |
| ListItems | server streaming |
| BulkCreate | client streaming |
| EchoWatch | bidirectional |

Ошибки: `ALREADY_EXISTS`, `INVALID_ARGUMENT`, `NOT_FOUND`, `DEADLINE_EXCEEDED`.

TLS не используется (только loopback). В проде нужны TLS и аутентификация.

## Команды

```powershell
# Генерация stubs
.\scripts\generate_kt12_proto.ps1

# Диагностика TC-12-01
.\scripts\run_kt12.ps1 -DiagnosticOnly

# Полный suite
.\scripts\run_kt12.ps1

# Сервер вручную (порт 50051) + CLI
cd grpc
..\.venv\Scripts\python.exe -m server --port 50051
# другой терминал:
..\.venv\Scripts\python.exe client\cli.py --target 127.0.0.1:50051
```
