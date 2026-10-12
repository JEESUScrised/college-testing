"""Do NOT rebuild automated/ from corrupted crossplatform/dom captures.

Canonical visual evidence for KT09 is already under:
  screenshots/kt09/automated/windows/
  screenshots/kt09/automated/android/

Those frames were captured with nativeWebScreenshot=false (ChromeDriver web
screenshot / Firefox Selenium). Older crossplatform/dom PNG files with
nativeWebScreenshot=true are GPU-glitched / dialog-obscured and must not be
copied into automated/.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTO_WIN = ROOT / "screenshots" / "kt09" / "automated" / "windows"
AUTO_AND = ROOT / "screenshots" / "kt09" / "automated" / "android"
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


def main() -> None:
    missing: list[str] = []
    for folder in (AUTO_WIN, AUTO_AND):
        for name in REQUIRED:
            path = folder / name
            if not path.is_file() or path.stat().st_size < 8_000:
                missing.append(str(path))
    if missing:
        raise SystemExit(
            "Canonical automated screenshots missing or too small:\n"
            + "\n".join(missing)
            + "\nRecapture with scripts/capture_kt09_android_visual.py "
            "and/or scripts/capture_kt09_visual_evidence.py"
        )
    print("OK: automated Windows/Android 8+8 screenshots present.")
    print("Refusing to copy from crossplatform/dom (historical GPU/dialog corruption).")


if __name__ == "__main__":
    main()
