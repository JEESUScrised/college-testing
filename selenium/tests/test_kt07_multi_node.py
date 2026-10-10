"""KT07 remediation — multi-browser sessions via Hub + multiple Nodes.

Run against Hub with ≥2 registered nodes (start_hub_multi_node.ps1).
Parallel overlap evidence is produced by scripts/run_kt07_parallel_proof.py.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts" / "kt07"
SHOTS = Path(__file__).resolve().parents[2] / "screenshots" / "kt07" / "multi"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@pytest.fixture(params=["chrome", "firefox"])
def multi_grid_driver(request, grid_url, page_load_strategy):
    """Independent RemoteWebDriver per browser (not tied to --browser)."""
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions

    browser = request.param
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1400,1000")
        options.add_argument("--disable-notifications")
    else:
        options = FirefoxOptions()
    options.page_load_strategy = page_load_strategy
    options.set_capability("se:name", f"KT07-multi:{request.node.name}")
    options.set_capability("se:kt", "07-multi")

    started = _utc_now()
    drv = webdriver.Remote(command_executor=grid_url, options=options)
    assert isinstance(drv, RemoteWebDriver)
    drv.set_page_load_timeout(30)
    try:
        drv.set_window_size(1400, 1000)
    except Exception:
        pass

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    caps = dict(drv.capabilities)
    meta = {
        "test": request.node.name,
        "browser": browser,
        "session_id": drv.session_id,
        "started_utc": started,
        "command_executor": grid_url,
        "browserName": caps.get("browserName"),
        "se:nodeUri": caps.get("se:nodeUri"),
        "platformName": caps.get("platformName"),
    }
    (ARTIFACTS / f"multi_session_{browser}_{drv.session_id[:8]}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    request.node._kt07_browser = browser  # type: ignore[attr-defined]
    try:
        yield drv
    finally:
        meta["ended_utc"] = _utc_now()
        (ARTIFACTS / f"multi_session_{browser}_{drv.session_id[:8]}.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        drv.quit()


@pytest.fixture
def multi_wait(multi_grid_driver):
    return WebDriverWait(multi_grid_driver, 12)


def _shot(driver, browser: str, name: str) -> None:
    SHOTS.mkdir(parents=True, exist_ok=True)
    assert driver.save_screenshot(str(SHOTS / f"{browser}_{name}.png"))


@pytest.mark.kt07
@pytest.mark.kt07_multi
def test_multi_remote_session(multi_grid_driver, request):
    browser = request.node._kt07_browser  # type: ignore[attr-defined]
    assert multi_grid_driver.session_id
    caps = multi_grid_driver.capabilities
    name = (caps.get("browserName") or "").lower()
    if browser == "chrome":
        assert name in {"chrome", "chromium"}
    else:
        assert "firefox" in name
    _shot(multi_grid_driver, browser, "01_session")


@pytest.mark.kt07
@pytest.mark.kt07_multi
def test_multi_navigate_fixture(multi_grid_driver, multi_wait, fixture_http_url, request):
    browser = request.node._kt07_browser  # type: ignore[attr-defined]
    url = fixture_http_url("kt07", "index.html")
    multi_grid_driver.get(url)
    multi_wait.until(EC.title_is("KT07 Grid Landing"))
    heading = multi_wait.until(EC.visibility_of_element_located((By.ID, "heading")))
    assert heading.text.strip() == "Selenium Grid KT07"
    _shot(multi_grid_driver, browser, "02_landing")
