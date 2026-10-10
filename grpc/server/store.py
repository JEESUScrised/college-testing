"""Thread-safe in-memory inventory repository."""

from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass
class ItemRecord:
    id: str
    name: str
    quantity: int
    category: str


class InventoryStore:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._items: dict[str, ItemRecord] = {}

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def create(self, item: ItemRecord) -> ItemRecord:
        with self._lock:
            if item.id in self._items:
                raise KeyError(f"exists:{item.id}")
            self._items[item.id] = item
            return item

    def get(self, item_id: str) -> ItemRecord:
        with self._lock:
            if item_id not in self._items:
                raise LookupError(item_id)
            return self._items[item_id]

    def update_stock(self, item_id: str, delta: int) -> ItemRecord:
        with self._lock:
            if item_id not in self._items:
                raise LookupError(item_id)
            current = self._items[item_id]
            new_qty = current.quantity + delta
            if new_qty < 0:
                raise ValueError("quantity would become negative")
            updated = ItemRecord(
                id=current.id,
                name=current.name,
                quantity=new_qty,
                category=current.category,
            )
            self._items[item_id] = updated
            return updated

    def list_items(self, category_filter: str = "") -> list[ItemRecord]:
        with self._lock:
            items = list(self._items.values())
        if category_filter:
            items = [i for i in items if i.category == category_filter]
        return sorted(items, key=lambda i: i.id)
