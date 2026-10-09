"""Capture approved KT08 baselines with a real Chrome Selenium session.

Usage (from repo root):
  .\\.venv\\Scripts\\python.exe selenium\\visual\\generate_kt08_baselines.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "selenium" / "fixtures" / "kt08"
BASELINES = ROOT / "selenium" / "baselines" / "kt08"
VIEWPORT = (1400, 1000)


def main() -> None:
    BASELINES.mkdir(parents=True, exist_ok=True)
    home = (FIXTURES / "home.html").resolve().as_uri()

    options = Options()
    options.add_argument(f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}")
    options.add_argument("--disable-notifications")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--force-device-scale-factor=1")
    options.add_argument("--high-dpi-support=1")

    driver = webdriver.Chrome(options=options)
    try:
        driver.set_window_size(*VIEWPORT)
        driver.get(home)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "heading")))
        target = BASELINES / "home_baseline.png"
        assert driver.save_screenshot(str(target)), f"Failed to save {target}"
        with ImageOpenSafe(target) as size:
            meta = {
                "file": target.name,
                "source_fixture": "selenium/fixtures/kt08/home.html",
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "browser": "chrome",
                "window_size": list(VIEWPORT),
                "image_size": list(size),
                "tool": "selenium/visual/generate_kt08_baselines.py",
                "note": "Approved baseline for KT08 visual regression. Do not overwrite on test failure.",
            }
        (BASELINES / "baseline_manifest.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Wrote {target} size={size}")
        print(f"Manifest: {BASELINES / 'baseline_manifest.json'}")
    finally:
        driver.quit()


class ImageOpenSafe:
    def __init__(self, path: Path) -> None:
        from PIL import Image

        self._img = Image.open(path)
        self._img.load()

    def __enter__(self):
        return self._img.size

    def __exit__(self, *args):
        self._img.close()


if __name__ == "__main__":
    main()
