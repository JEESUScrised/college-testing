"""KT09 Android public-web BASIC smoke via adb intent (no visual submission).

Opens SauceDemo in Chrome and records focus/package evidence.
Does NOT write submission screenshots — those live in
screenshots/kt09/automated/android/ (ChromeDriver web capture).

Historical adb screencaps (Chrome dialogs / GPU issues) were archived under
screenshots/kt09/archive/unusable-visual/.
"""

from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "mobile" / "artifacts" / "kt09"
AUTO = ROOT / "screenshots" / "kt09" / "automated" / "android"
BASE_URL = "https://www.saucedemo.com/"
UDID = "emulator-5554"


def adb(*args: str) -> str:
    cmd = ["adb", "-s", UDID, *args]
    return subprocess.check_output(
        cmd, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace"
    )


def current_focus() -> str:
    out = adb("shell", "sh", "-c", "dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
    for line in out.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    adb("shell", "am", "force-stop", "com.android.chrome")
    adb(
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        BASE_URL,
        "com.android.chrome",
    )
    time.sleep(3)
    focus = current_focus()
    chrome_ok = "com.android.chrome" in focus
    auto_ok = all(
        (AUTO / name).is_file() and (AUTO / name).stat().st_size > 8_000
        for name in (
            "01_login.png",
            "02_inventory.png",
            "03_product_details.png",
            "04_added_to_cart.png",
            "05_cart.png",
            "06_menu.png",
            "07_checkout_form.png",
            "08_order_confirmation.png",
        )
    )
    evidence = {
        "started_utc": started,
        "udid": UDID,
        "url": BASE_URL,
        "mode": "adb_intent_focus_only",
        "focus": focus,
        "chrome_focused": chrome_ok,
        "automated_visual_present": auto_ok,
        "visual_path": "screenshots/kt09/automated/android/",
        "note": (
            "Smoke checks Chrome focus only. Submission visuals are automated "
            "ChromeDriver web screenshots (nativeWebScreenshot=false)."
        ),
        "result": "PASS" if chrome_ok and auto_ok else ("PARTIAL" if chrome_ok else "FAIL"),
    }
    out = ARTIFACTS / "android_web_smoke.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if evidence["result"] in {"PASS", "PARTIAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
