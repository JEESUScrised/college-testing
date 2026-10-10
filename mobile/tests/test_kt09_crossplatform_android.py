"""KT09 remediation — Android public web smoke (BASIC cross-platform matrix).

Uses native Chrome + VIEW intent (no ChromeDriver) via scripts/run_kt09_android_web_smoke.py
because emulator Chrome 134 has no matching chromedriver in this environment.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = PROJECT_ROOT / "scripts" / "run_kt09_android_web_smoke.py"
EVIDENCE = PROJECT_ROOT / "mobile" / "artifacts" / "kt09" / "android_web_smoke.json"
SHOTS = PROJECT_ROOT / "screenshots" / "kt09" / "crossplatform"


@pytest.mark.kt09
@pytest.mark.kt09_xp
def test_kt09_android_sauce_public_web_smoke():
    assert SCRIPT.is_file(), SCRIPT
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
    assert proc.returncode == 0, proc.stderr or proc.stdout
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert data["result"] in {"PASS", "PARTIAL"}
    focus = f"{data.get('focus_1','')} {data.get('focus_2','')}"
    assert "com.android.chrome" in focus
    assert (SHOTS / "android_chrome_01_login.png").is_file()
    assert (SHOTS / "android_chrome_02_inventory.png").is_file()
