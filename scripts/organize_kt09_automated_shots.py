"""Curate readable Android screenshots into screenshots/kt09/automated/android."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOM = ROOT / "screenshots" / "kt09" / "crossplatform" / "dom"
OUT = ROOT / "screenshots" / "kt09" / "automated" / "android"

# Prefer newest DOM suite captures; sizes/readability checked later by human/DOCX audit.
MAPPING = {
    "01_login.png": "tc09_w02_login_form.png",
    "02_inventory.png": "tc09_w04_inventory.png",
    "03_product_details.png": "tc09_w05_product.png",
    "04_added_to_cart.png": "tc09_w06_add_cart.png",
    "05_cart.png": "tc09_w07_cart.png",
    "06_menu.png": "tc09_w09_menu.png",
    "07_checkout_form.png": "tc09_w08_checkout_validation.png",
    # Order confirmation was captured in Windows automated set; Android suite
    # historically stops at checkout validation. Prefer inventory-quality historical
    # journey only if confirmation missing — leave 08 for optional copy.
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Prefer historically readable inventory if current inventory is tiny/glitched.
    preferred_inventory = DOM / "dom_02_inventory.png"
    for dest_name, src_name in MAPPING.items():
        src = DOM / src_name
        if not src.is_file():
            print(f"MISSING {src}")
            continue
        # For inventory, use known-good historical if newer is smaller/worse.
        if dest_name == "02_inventory.png" and preferred_inventory.is_file():
            if preferred_inventory.stat().st_size > src.stat().st_size:
                src = preferred_inventory
        dest = OUT / dest_name
        shutil.copy2(src, dest)
        print(f"{dest_name} <- {src.name} ({dest.stat().st_size})")


if __name__ == "__main__":
    main()
