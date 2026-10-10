"""Pytest fixtures: real gRPC server on 127.0.0.1:<free-port> + generated stub."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import grpc
import pytest

KT12_ROOT = Path(__file__).resolve().parent
GENERATED = KT12_ROOT / "generated"
SERVER_DIR = KT12_ROOT / "server"
ARTIFACTS = KT12_ROOT / "artifacts" / "kt12"

for path in (str(GENERATED), str(SERVER_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

import inventory_pb2  # noqa: E402
import inventory_pb2_grpc  # noqa: E402
from service import create_server  # noqa: E402
from store import InventoryStore  # noqa: E402


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "kt12: KT12 gRPC InventoryService tests")
    ARTIFACTS.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def inventory_env():
    """Start a fresh in-memory InventoryService and yield (stub, target, channel)."""
    store = InventoryStore()
    server, port = create_server(store, host="127.0.0.1", port=0)
    server.start()
    target = f"127.0.0.1:{port}"
    channel = grpc.insecure_channel(target)
    grpc.channel_ready_future(channel).result(timeout=5)
    stub = inventory_pb2_grpc.InventoryServiceStub(channel)
    try:
        yield {
            "stub": stub,
            "target": target,
            "channel": channel,
            "port": port,
            "store": store,
            "pb2": inventory_pb2,
        }
    finally:
        channel.close()
        server.stop(grace=1).wait(timeout=5)


@pytest.fixture
def stub(inventory_env):
    return inventory_env["stub"]


@pytest.fixture
def pb2(inventory_env):
    return inventory_env["pb2"]


@pytest.fixture
def evidence_log(request):
    """Append structured evidence lines for the DOCX / artifacts."""
    lines: list[dict] = []

    def _log(event: str, **payload):
        entry = {"test": request.node.name, "event": event, **payload}
        lines.append(entry)

    yield _log

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    path = ARTIFACTS / "evidence.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        for entry in lines:
            fh.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
