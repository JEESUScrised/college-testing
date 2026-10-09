"""Resolve ChromeDriver via Selenium Manager and cache it under selenium/drivers/."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    target_dir = root / "selenium" / "drivers"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "chromedriver.exe"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.page_load_strategy = "none"

    # Trigger Selenium Manager while network is available.
    service = Service()
    driver = webdriver.Chrome(options=options, service=service)
    try:
        driver_path = Path(driver.service.path)
    finally:
        driver.quit()

    if not driver_path.is_file():
        print(f"ERROR: Selenium Manager did not provide chromedriver: {driver_path}")
        return 1

    shutil.copy2(driver_path, target)
    print(f"OK: cached ChromeDriver -> {target}")
    print(f"SOURCE: {driver_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
