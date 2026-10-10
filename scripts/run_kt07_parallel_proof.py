"""Prove overlapping Chrome + Firefox RemoteWebDriver sessions on Grid.

Starts two sessions concurrently, holds both for a few seconds, navigates
each to the KT07 fixture, and writes overlap evidence JSON.
"""

from __future__ import annotations

import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "selenium" / "fixtures"
ARTIFACTS = ROOT / "selenium" / "artifacts" / "kt07"
SHOTS = ROOT / "screenshots" / "kt07" / "multi"
GRID_URL = "http://127.0.0.1:4444"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def start_fixture_server() -> tuple[ThreadingHTTPServer, str]:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(FIXTURES), **kwargs)

        def log_message(self, fmt, *args):  # noqa: A003
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    return server, base


def run_browser(browser: str, base_url: str, hold_sec: float = 4.0) -> dict:
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1400,1000")
    else:
        options = FirefoxOptions()
    options.set_capability("se:name", f"KT07-parallel-{browser}")
    options.set_capability("se:kt", "07-parallel")

    record: dict = {"browser": browser, "started_utc": utc_now()}
    drv = webdriver.Remote(command_executor=GRID_URL, options=options)
    record["session_id"] = drv.session_id
    caps = dict(drv.capabilities)
    record["browserName"] = caps.get("browserName")
    record["se:nodeUri"] = caps.get("se:nodeUri")
    record["hold_started_utc"] = utc_now()
    try:
        time.sleep(hold_sec)  # intentional overlap window for both sessions
        wait = WebDriverWait(drv, 15)
        drv.get(f"{base_url}/kt07/index.html")
        wait.until(EC.title_is("KT07 Grid Landing"))
        heading = wait.until(EC.visibility_of_element_located((By.ID, "heading")))
        record["heading"] = heading.text.strip()
        SHOTS.mkdir(parents=True, exist_ok=True)
        path = SHOTS / f"parallel_{browser}_overlap.png"
        drv.save_screenshot(str(path))
        record["screenshot"] = str(path.relative_to(ROOT)).replace("\\", "/")
    finally:
        record["hold_ended_utc"] = utc_now()
        drv.quit()
        record["ended_utc"] = utc_now()
    return record


def intervals_overlap(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    return a_start < b_end and b_start < a_end


def main() -> int:
    # Grid readiness
    import urllib.request

    try:
        with urllib.request.urlopen(f"{GRID_URL}/status", timeout=5) as resp:
            status = json.loads(resp.read().decode())
    except Exception as exc:  # noqa: BLE001
        print(f"Grid unavailable at {GRID_URL}: {exc}", file=sys.stderr)
        return 2

    ready = status.get("value", {}).get("ready")
    nodes = status.get("value", {}).get("nodes") or []
    print(f"Grid ready={ready} nodes={len(nodes)}")
    if not ready:
        return 2

    server, base = start_fixture_server()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futs = {
                pool.submit(run_browser, "chrome", base): "chrome",
                pool.submit(run_browser, "firefox", base): "firefox",
            }
            for fut in as_completed(futs):
                results.append(fut.result())
    finally:
        server.shutdown()

    by_browser = {r["browser"]: r for r in results}
    chrome = by_browser["chrome"]
    firefox = by_browser["firefox"]
    overlap = intervals_overlap(
        chrome["hold_started_utc"],
        chrome["hold_ended_utc"],
        firefox["hold_started_utc"],
        firefox["hold_ended_utc"],
    )
    evidence = {
        "grid_url": GRID_URL,
        "nodes_registered": len(nodes),
        "parallel_overlap": overlap,
        "sessions": results,
        "node_uris": sorted(
            {r.get("se:nodeUri") for r in results if r.get("se:nodeUri")}
        ),
    }
    out = ARTIFACTS / "parallel_overlap_evidence.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    print(f"Wrote {out}")
    if not overlap:
        print("ERROR: sessions did not overlap", file=sys.stderr)
        return 1
    if chrome.get("heading") != "Selenium Grid KT07" or firefox.get("heading") != "Selenium Grid KT07":
        print("ERROR: fixture assertion failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
