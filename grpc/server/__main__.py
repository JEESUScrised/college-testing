"""Run InventoryService independently: python -m server (from grpc/ with paths set)."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "generated"))
sys.path.insert(0, str(ROOT / "server"))

from service import create_server  # noqa: E402
from store import InventoryStore  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="KT12 Inventory gRPC server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=50051)
    args = parser.parse_args()
    store = InventoryStore()
    server, bound = create_server(store, host=args.host, port=args.port)
    server.start()
    print(f"InventoryService listening on {args.host}:{bound} (insecure)", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("Shutting down...", flush=True)
        server.stop(grace=2)


if __name__ == "__main__":
    main()
