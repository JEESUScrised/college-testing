"""KT12 — exactly 10 automated tests against a real Inventory gRPC service."""

from __future__ import annotations

import grpc
import pytest

pytestmark = pytest.mark.kt12


def _item_dict(item) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "quantity": item.quantity,
        "category": item.category,
    }


@pytest.mark.kt12
def test_tc12_01_create_item_successfully(stub, pb2, evidence_log):
    """TC-12-01 — Create item successfully (unary)."""
    req = pb2.CreateItemRequest(
        id="sku-001", name="USB Cable", quantity=10, category="cables"
    )
    evidence_log("request", rpc="CreateItem", payload=_item_dict(req))
    item = stub.CreateItem(req)
    evidence_log("response", rpc="CreateItem", payload=_item_dict(item), status="OK")
    assert item.id == "sku-001"
    assert item.name == "USB Cable"
    assert item.quantity == 10
    assert item.category == "cables"


@pytest.mark.kt12
def test_tc12_02_retrieve_existing_item(stub, pb2, evidence_log):
    """TC-12-02 — Retrieve an existing item (unary)."""
    stub.CreateItem(
        pb2.CreateItemRequest(id="sku-002", name="Mouse", quantity=3, category="peripherals")
    )
    got = stub.GetItem(pb2.GetItemRequest(id="sku-002"))
    evidence_log("response", rpc="GetItem", payload=_item_dict(got), status="OK")
    assert got.id == "sku-002"
    assert got.name == "Mouse"
    assert got.quantity == 3
    assert got.category == "peripherals"


@pytest.mark.kt12
def test_tc12_03_reject_duplicate_item_id(stub, pb2, evidence_log):
    """TC-12-03 — Reject duplicate item ID (ALREADY_EXISTS)."""
    req = pb2.CreateItemRequest(id="sku-dup", name="A", quantity=1, category="x")
    stub.CreateItem(req)
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.CreateItem(req)
    err = exc_info.value
    evidence_log(
        "error",
        rpc="CreateItem",
        status=str(err.code()),
        details=err.details(),
    )
    assert err.code() == grpc.StatusCode.ALREADY_EXISTS


@pytest.mark.kt12
def test_tc12_04_reject_invalid_item_data(stub, pb2, evidence_log):
    """TC-12-04 — Reject invalid item data (INVALID_ARGUMENT)."""
    with pytest.raises(grpc.RpcError) as empty_name:
        stub.CreateItem(
            pb2.CreateItemRequest(id="bad-1", name="  ", quantity=1, category="x")
        )
    assert empty_name.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    evidence_log(
        "error",
        rpc="CreateItem",
        case="empty_name",
        status=str(empty_name.value.code()),
    )

    with pytest.raises(grpc.RpcError) as neg_qty:
        stub.CreateItem(
            pb2.CreateItemRequest(id="bad-2", name="Widget", quantity=-5, category="x")
        )
    assert neg_qty.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    evidence_log(
        "error",
        rpc="CreateItem",
        case="negative_quantity",
        status=str(neg_qty.value.code()),
    )


@pytest.mark.kt12
def test_tc12_05_retrieve_missing_item(stub, pb2, evidence_log):
    """TC-12-05 — Retrieve a missing item (NOT_FOUND)."""
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.GetItem(pb2.GetItemRequest(id="no-such-id"))
    err = exc_info.value
    evidence_log("error", rpc="GetItem", status=str(err.code()), details=err.details())
    assert err.code() == grpc.StatusCode.NOT_FOUND


@pytest.mark.kt12
def test_tc12_06_update_inventory_stock(stub, pb2, evidence_log):
    """TC-12-06 — Update inventory stock (unary + re-fetch)."""
    stub.CreateItem(
        pb2.CreateItemRequest(id="sku-stock", name="SSD", quantity=20, category="storage")
    )
    updated = stub.UpdateStock(pb2.UpdateStockRequest(id="sku-stock", delta=-7))
    evidence_log("response", rpc="UpdateStock", payload=_item_dict(updated), status="OK")
    assert updated.quantity == 13
    fetched = stub.GetItem(pb2.GetItemRequest(id="sku-stock"))
    assert fetched.quantity == 13


@pytest.mark.kt12
def test_tc12_07_server_side_streaming(stub, pb2, evidence_log):
    """TC-12-07 — Server-side streaming ListItems."""
    for i, (sku, name, cat) in enumerate(
        [
            ("s1", "Alpha", "a"),
            ("s2", "Beta", "b"),
            ("s3", "Gamma", "a"),
        ],
        start=1,
    ):
        stub.CreateItem(
            pb2.CreateItemRequest(id=sku, name=name, quantity=i, category=cat)
        )

    stream = stub.ListItems(pb2.ListItemsRequest(category_filter=""))
    items = list(stream)
    ids = [it.id for it in items]
    evidence_log(
        "stream",
        rpc="ListItems",
        count=len(items),
        ids=ids,
        status="OK",
    )
    assert len(items) == 3
    assert sorted(ids) == ["s1", "s2", "s3"]
    assert len(set(ids)) == 3

    filtered = list(stub.ListItems(pb2.ListItemsRequest(category_filter="a")))
    assert sorted(it.id for it in filtered) == ["s1", "s3"]


@pytest.mark.kt12
def test_tc12_08_client_side_streaming(stub, pb2, evidence_log):
    """TC-12-08 — Client-side streaming BulkCreate."""

    def request_iter():
        for sku, name, qty in [
            ("b1", "Bulk One", 1),
            ("b2", "Bulk Two", 2),
            ("b3", "Bulk Three", 3),
        ]:
            yield pb2.CreateItemRequest(
                id=sku, name=name, quantity=qty, category="bulk"
            )

    resp = stub.BulkCreate(request_iter())
    evidence_log(
        "response",
        rpc="BulkCreate",
        created_count=resp.created_count,
        ids=list(resp.ids),
        status="OK",
    )
    assert resp.created_count == 3
    assert list(resp.ids) == ["b1", "b2", "b3"]
    for sku, qty in [("b1", 1), ("b2", 2), ("b3", 3)]:
        got = stub.GetItem(pb2.GetItemRequest(id=sku))
        assert got.quantity == qty
        assert got.category == "bulk"


@pytest.mark.kt12
def test_tc12_09_bidirectional_streaming(stub, pb2, evidence_log):
    """TC-12-09 — Bidirectional EchoWatch (1:1 ordered responses)."""
    stub.CreateItem(
        pb2.CreateItemRequest(id="w1", name="Watched", quantity=9, category="watch")
    )

    def requests():
        yield pb2.WatchRequest(item_id="w1", note="first")
        yield pb2.WatchRequest(item_id="missing", note="second")
        yield pb2.WatchRequest(item_id="w1", note="third")

    responses = list(stub.EchoWatch(requests()))
    evidence_log(
        "bidi",
        rpc="EchoWatch",
        responses=[
            {
                "item_id": r.item_id,
                "note": r.note,
                "status": r.status,
                "quantity": r.quantity,
            }
            for r in responses
        ],
    )
    assert len(responses) == 3
    assert responses[0].item_id == "w1"
    assert responses[0].note == "first"
    assert responses[0].status == "FOUND"
    assert responses[0].quantity == 9
    assert responses[1].item_id == "missing"
    assert responses[1].note == "second"
    assert responses[1].status == "MISSING"
    assert responses[2].item_id == "w1"
    assert responses[2].note == "third"
    assert responses[2].status == "FOUND"


@pytest.mark.kt12
def test_tc12_10_rpc_deadline_exceeded(stub, pb2, evidence_log):
    """TC-12-10 — SlowPing with short deadline → DEADLINE_EXCEEDED."""
    # Server waits 800ms; client deadline 100ms — deterministic and non-flaky margin.
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.SlowPing(
            pb2.SlowPingRequest(delay_ms=800),
            timeout=0.1,
        )
    err = exc_info.value
    evidence_log(
        "error",
        rpc="SlowPing",
        status=str(err.code()),
        details=err.details(),
        client_timeout_s=0.1,
        server_delay_ms=800,
    )
    assert err.code() == grpc.StatusCode.DEADLINE_EXCEEDED
