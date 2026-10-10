"""Simple CLI client demonstrating one successful CreateItem + GetItem RPC."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import grpc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "generated"))

import inventory_pb2  # noqa: E402
import inventory_pb2_grpc  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="KT12 Inventory gRPC CLI")
    parser.add_argument("--target", default="127.0.0.1:50051")
    parser.add_argument("--id", default="demo-1")
    parser.add_argument("--name", default="Demo Widget")
    parser.add_argument("--quantity", type=int, default=5)
    parser.add_argument("--category", default="demo")
    args = parser.parse_args()

    channel = grpc.insecure_channel(args.target)
    try:
        grpc.channel_ready_future(channel).result(timeout=5)
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        created = stub.CreateItem(
            inventory_pb2.CreateItemRequest(
                id=args.id,
                name=args.name,
                quantity=args.quantity,
                category=args.category,
            )
        )
        print("CreateItem OK:", created)
        got = stub.GetItem(inventory_pb2.GetItemRequest(id=args.id))
        print("GetItem OK:", got)
        return 0
    except grpc.RpcError as exc:
        print(f"RPC failed: {exc.code()} {exc.details()}", file=sys.stderr)
        return 1
    finally:
        channel.close()


if __name__ == "__main__":
    raise SystemExit(main())
