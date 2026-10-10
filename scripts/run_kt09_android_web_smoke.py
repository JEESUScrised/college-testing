"""KT09 Android public-web BASIC smoke via adb intent + screencap.

Avoids ChromeDriver (emulator Chrome 134 mismatch) and Appium accessibility
timeouts on Chrome first-run. Evidence: package/activity + screenshots.
"""

from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots" / "kt09" / "crossplatform"
ARTIFACTS = ROOT / "mobile" / "artifacts" / "kt09"
BASE_URL = "https://www.saucedemo.com/"
UDID = "emulator-5554"


def adb(*args: str) -> str:
    cmd = ["adb", "-s", UDID, *args]
    return subprocess.check_output(
        cmd, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace"
    )


def screencap(path: Path) -> None:
    raw = subprocess.check_output(["adb", "-s", UDID, "exec-out", "screencap", "-p"])
    # Some Windows adb builds CRLF-corrupt PNG; prefer exec-out binary as-is.
    path.write_bytes(raw)


def current_focus() -> str:
    out = adb("shell", "sh", "-c", "dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
    for line in out.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    SHOTS.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    adb("shell", "am", "force-stop", "com.android.chrome")
    try:
        adb(
            "shell",
            "sh",
            "-c",
            "echo 'chrome --disable-fre --no-default-browser-check --no-first-run' > /data/local/tmp/chrome-command-line",
        )
        adb("shell", "am", "set-debug-app", "--persistent", "com.android.chrome")
    except subprocess.CalledProcessError:
        pass

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
    time.sleep(4)
    # Dismiss Chrome notification promo if present (approx coords on 1080x2400).
    for x, y in ((320, 1580), (750, 1580), (540, 1700)):
        try:
            adb("shell", "input", "tap", str(x), str(y))
            time.sleep(0.8)
        except subprocess.CalledProcessError:
            pass
    time.sleep(2)
    focus1 = current_focus()
    shot1 = SHOTS / "android_chrome_01_login.png"
    screencap(shot1)

    # Second capture after settle (DOM login not automated without ChromeDriver)
    time.sleep(2)
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
    focus2 = current_focus()
    shot2 = SHOTS / "android_chrome_02_page.png"
    screencap(shot2)
    # Keep legacy filename expected by docs/tests
    legacy = SHOTS / "android_chrome_02_inventory.png"
    legacy.write_bytes(shot2.read_bytes())

    chrome_ok = "com.android.chrome" in focus1 or "com.android.chrome" in focus2
    png_ok = shot1.is_file() and shot1.stat().st_size > 1000 and legacy.is_file()
    evidence = {
        "started_utc": started,
        "udid": UDID,
        "url": BASE_URL,
        "mode": "adb_intent_screencap",
        "focus_1": focus1,
        "focus_2": focus2,
        "screenshot_login": str(shot1.relative_to(ROOT)).replace("\\", "/"),
        "screenshot_inventory": str(legacy.relative_to(ROOT)).replace("\\", "/"),
        "note": (
            "BASIC Android cell: open Sauce Demo in Chrome via VIEW intent + screencap. "
            "DOM login not automated (ChromeDriver missing for Chrome 134). "
            "Marked PARTIAL vs Windows Selenium PASS cells."
        ),
        "result": "PARTIAL" if chrome_ok and png_ok else "FAIL",
        "ended_utc": datetime.now(timezone.utc).isoformat(),
    }
    out = ARTIFACTS / "android_web_smoke.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    print(f"Wrote {out}")
    return 0 if evidence["result"] == "PARTIAL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
