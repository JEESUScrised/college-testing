"""Regenerate Allure HTML if needed and capture overview/suites over HTTP."""

from __future__ import annotations

import http.server
import socketserver
import subprocess
import threading
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "selenium" / "artifacts" / "kt08" / "allure-results"
REPORT = ROOT / "selenium" / "artifacts" / "kt08" / "allure-report"
SHOTS = ROOT / "screenshots" / "kt08"
ALLURE = Path(r"C:\allure\allure-2.37.0\bin\allure.bat")


def ensure_report() -> None:
    if not any(RESULTS.glob("*-result.json")):
        raise SystemExit(f"No allure results in {RESULTS}; run scripts/run_kt08.ps1 first")
    if REPORT.is_dir():
        # regenerate clean
        subprocess.run(
            [str(ALLURE), "generate", str(RESULTS), "-o", str(REPORT), "--clean"],
            check=True,
        )
    else:
        subprocess.run(
            [str(ALLURE), "generate", str(RESULTS), "-o", str(REPORT), "--clean"],
            check=True,
        )


def serve(directory: Path, port: int = 8765):
    handler = http.server.SimpleHTTPRequestHandler
    # Python 3.7+ directory= 
    class DirHandler(handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

    httpd = socketserver.TCPServer(("127.0.0.1", port), DirHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def main() -> None:
    ensure_report()
    httpd = serve(REPORT, 8765)
    opts = Options()
    opts.add_argument("--window-size=1400,1000")
    opts.add_argument("--disable-gpu")
    drv = webdriver.Chrome(options=opts)
    try:
        wait = WebDriverWait(drv, 40)
        drv.get("http://127.0.0.1:8765/index.html")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Wait until widgets leave Loading...
        wait.until(
            lambda d: "Loading..." not in d.page_source
            or d.execute_script(
                "return document.body.innerText.indexOf('Loading...') === -1 "
                "|| document.querySelectorAll('.widget__title').length > 0;"
            )
        )
        # Stronger: wait for non-empty widget content / summary numbers
        for _ in range(30):
            text = drv.execute_script("return document.body.innerText || '';")
            if "Loading..." not in text and ("passed" in text.lower() or "Passed" in text or "Total" in text or "Suites" in text):
                # also check no pure Loading placeholders
                if text.count("Loading...") == 0:
                    break
            time.sleep(0.5)
        time.sleep(1.0)
        p1 = SHOTS / "allure_01_overview.png"
        assert drv.save_screenshot(str(p1))
        assert p1.stat().st_size > 20_000
        body = drv.execute_script("return document.body.innerText || '';")
        assert "Loading..." not in body, "Overview still loading"
        print("overview OK", p1.stat().st_size)

        # Navigate to Suites
        clicked = False
        for el in drv.find_elements(By.CSS_SELECTOR, "a, .side-nav__link, [href*='suites']"):
            href = (el.get_attribute("href") or "") + " " + (el.text or "")
            if "suites" in href.lower() or (el.text or "").strip().lower() == "suites":
                try:
                    el.click()
                    clicked = True
                    break
                except Exception:
                    continue
        if not clicked:
            drv.get("http://127.0.0.1:8765/index.html#suites")
        time.sleep(1.5)
        for _ in range(30):
            text = drv.execute_script("return document.body.innerText || '';")
            if "404" not in text and "Loading..." not in text and len(text) > 80:
                break
            time.sleep(0.5)
        body2 = drv.execute_script("return document.body.innerText || '';")
        assert "404" not in body2, body2[:200]
        p2 = SHOTS / "allure_02_suites.png"
        assert drv.save_screenshot(str(p2))
        assert p2.stat().st_size > 15_000
        print("suites OK", p2.stat().st_size, "url=", drv.current_url)
    finally:
        drv.quit()
        httpd.shutdown()


if __name__ == "__main__":
    main()
