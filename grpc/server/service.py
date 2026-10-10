"""InventoryServiceServicer — real gRPC service implementation."""

from __future__ import annotations

import time
from concurrent import futures

import grpc

import inventory_pb2
import inventory_pb2_grpc
from store import InventoryStore, ItemRecord


def _to_proto(item: ItemRecord) -> inventory_pb2.Item:
    return inventory_pb2.Item(
        id=item.id,
        name=item.name,
        quantity=item.quantity,
        category=item.category,
    )


def _validate_create(request: inventory_pb2.CreateItemRequest) -> None:
    if not request.id.strip():
        raise ValueError("id must be non-empty")
    if not request.name.strip():
        raise ValueError("name must be non-empty")
    if request.quantity < 0:
        raise ValueError("quantity must be >= 0")


class InventoryServicer(inventory_pb2_grpc.InventoryServiceServicer):
    def __init__(self, store: InventoryStore) -> None:
        self._store = store

    def CreateItem(self, request, context):  # noqa: N802
        try:
            _validate_create(request)
        except ValueError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        record = ItemRecord(
            id=request.id.strip(),
            name=request.name.strip(),
            quantity=int(request.quantity),
            category=(request.category or "").strip() or "general",
        )
        try:
            created = self._store.create(record)
        except KeyError:
            context.abort(
                grpc.StatusCode.ALREADY_EXISTS,
                f"item id already exists: {record.id}",
            )
        return _to_proto(created)

    def GetItem(self, request, context):  # noqa: N802
        if not request.id.strip():
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id must be non-empty")
        try:
            item = self._store.get(request.id.strip())
        except LookupError:
            context.abort(grpc.StatusCode.NOT_FOUND, f"item not found: {request.id}")
        return _to_proto(item)

    def UpdateStock(self, request, context):  # noqa: N802
        if not request.id.strip():
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id must be non-empty")
        try:
            updated = self._store.update_stock(request.id.strip(), int(request.delta))
        except LookupError:
            context.abort(grpc.StatusCode.NOT_FOUND, f"item not found: {request.id}")
        except ValueError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
        return _to_proto(updated)

    def ListItems(self, request, context):  # noqa: N802
        for item in self._store.list_items(request.category_filter.strip()):
            if context.is_active():
                yield _to_proto(item)

    def BulkCreate(self, request_iterator, context):  # noqa: N802
        created_ids: list[str] = []
        for req in request_iterator:
            if not context.is_active():
                break
            try:
                _validate_create(req)
            except ValueError as exc:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
            record = ItemRecord(
                id=req.id.strip(),
                name=req.name.strip(),
                quantity=int(req.quantity),
                category=(req.category or "").strip() or "general",
            )
            try:
                self._store.create(record)
            except KeyError:
                context.abort(
                    grpc.StatusCode.ALREADY_EXISTS,
                    f"item id already exists: {record.id}",
                )
            created_ids.append(record.id)
        return inventory_pb2.BulkCreateResponse(
            created_count=len(created_ids),
            ids=created_ids,
        )

    def EchoWatch(self, request_iterator, context):  # noqa: N802
        # Contract: one WatchResponse per WatchRequest, same order, same item_id/note.
        for req in request_iterator:
            if not context.is_active():
                break
            item_id = (req.item_id or "").strip()
            note = req.note or ""
            if not item_id:
                yield inventory_pb2.WatchResponse(
                    item_id="",
                    note=note,
                    status="INVALID",
                    quantity=-1,
                )
                continue
            try:
                item = self._store.get(item_id)
                status = "FOUND"
                qty = item.quantity
            except LookupError:
                status = "MISSING"
                qty = -1
            yield inventory_pb2.WatchResponse(
                item_id=item_id,
                note=note,
                status=status,
                quantity=qty,
            )

    def SlowPing(self, request, context):  # noqa: N802
        delay_ms = max(0, int(request.delay_ms))
        waited = 0
        step = 20
        while waited < delay_ms:
            if context.is_active() is False:
                # Client cancelled / deadline exceeded — stop early, no abort needed.
                return inventory_pb2.SlowPingResponse(
                    message="cancelled",
                    waited_ms=waited,
                )
            time.sleep(step / 1000.0)
            waited += step
        return inventory_pb2.SlowPingResponse(
            message="pong",
            waited_ms=min(waited, delay_ms),
        )


def create_server(store: InventoryStore, host: str = "127.0.0.1", port: int = 0):
    """Create and bind an insecure gRPC server; port=0 selects a free port."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(
        InventoryServicer(store), server
    )
    bound = server.add_insecure_port(f"{host}:{port}")
    if bound == 0:
        raise RuntimeError("failed to bind gRPC server port")
    return server, bound
