"""KT09 — Android public web smoke asserts canonical automated screenshots exist.

DOM assertions remain in test_kt09_android_chrome_dom.py (11 PASS suite).
Visual evidence for submission is screenshots/kt09/automated/android/,
captured with nativeWebScreenshot=false.
"""

from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTO = PROJECT_ROOT / "screenshots" / "kt09" / "automated" / "android"
REQUIRED = [
    "01_login.png",
    "02_inventory.png",
    "03_product_details.png",
    "04_added_to_cart.png",
    "05_cart.png",
    "06_menu.png",
    "07_checkout_form.png",
    "08_order_confirmation.png",
]


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_kt09_android_automated_visual_evidence_present():
    missing = [
        name
        for name in REQUIRED
        if not (AUTO / name).is_file() or (AUTO / name).stat().st_size < 8_000
    ]
    assert not missing, f"Missing/invalid automated Android screenshots: {missing}"
