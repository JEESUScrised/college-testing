"""КТ 08: визуальная регрессия Selenium + Pillow."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from visual.compare import compare_images, write_summary_row

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASELINES = PROJECT_ROOT / "selenium" / "baselines" / "kt08"
SHOTS = PROJECT_ROOT / "screenshots" / "kt08"
ARTIFACTS = PROJECT_ROOT / "selenium" / "artifacts" / "kt08"
SUMMARY = ARTIFACTS / "comparison_summary.jsonl"

# Fixed visual-test profile (must match baseline capture)
VIEWPORT = (1400, 1000)
COLOR_TOLERANCE = 12
MATCH_THRESHOLD_PERCENT = 0.75  # allow minor AA/font raster noise
MIN_DIFF_TEXT_COLOR = 0.3
MIN_DIFF_LAYOUT = 1.0
MIN_DIFF_SIGNIFICANT = 10.0


@pytest.fixture
def visual_driver(driver):
    """Local Chrome with fixed window size (same profile as baseline generator)."""
    driver.set_window_size(*VIEWPORT)
    return driver


@pytest.fixture
def visual_wait(visual_driver):
    from selenium.webdriver.support.ui import WebDriverWait

    return WebDriverWait(visual_driver, 10)


def _open_fixture(driver, wait, fixture_url, *parts: str) -> None:
    driver.get(fixture_url(*parts))
    wait.until(EC.visibility_of_element_located((By.ID, "heading")))


def _capture(driver, name: str) -> Path:
    SHOTS.mkdir(parents=True, exist_ok=True)
    path = SHOTS / f"{name}.png"
    assert driver.save_screenshot(str(path)), path
    return path


def _record(result, test_id: str, status: str) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    row = {
        "test_id": test_id,
        "status": status,
        **result.to_dict(),
    }
    write_summary_row(SUMMARY, row)
    (ARTIFACTS / f"{test_id}_result.json").write_text(
        json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8"
    )


@pytest.fixture(scope="session", autouse=True)
def _reset_summary():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    if SUMMARY.exists():
        SUMMARY.unlink()
    yield


@pytest.mark.kt08
def test_unchanged_page_matches_baseline(visual_driver, visual_wait, fixture_url):
    """Неизменённая страница совпадает с утверждённым baseline."""
    baseline = BASELINES / "home_baseline.png"
    assert baseline.is_file(), f"Missing baseline: {baseline}. Run generate_kt08_baselines.py"

    _open_fixture(visual_driver, visual_wait, fixture_url, "kt08", "home.html")
    actual = _capture(visual_driver, "01_home_actual")

    result = compare_images(
        baseline,
        actual,
        color_tolerance=COLOR_TOLERANCE,
        threshold_percent=MATCH_THRESHOLD_PERCENT,
        artifacts_dir=ARTIFACTS,
        name="01_match",
    )
    _record(result, "TC-08-01", "PASS" if result.matched else "FAIL")
    assert not result.dimension_mismatch, result.message
    assert result.matched, result.message


@pytest.mark.kt08
def test_text_or_color_change_detected(visual_driver, visual_wait, fixture_url):
    """Изменение текста/цвета кнопки обнаруживается сравнением."""
    baseline = BASELINES / "home_baseline.png"
    _open_fixture(visual_driver, visual_wait, fixture_url, "kt08", "home_text_color.html")
    actual = _capture(visual_driver, "02_text_color_actual")

    result = compare_images(
        baseline,
        actual,
        color_tolerance=COLOR_TOLERANCE,
        threshold_percent=MATCH_THRESHOLD_PERCENT,
        artifacts_dir=ARTIFACTS,
        name="02_text_color",
    )
    detected = (not result.matched) and (result.diff_percent >= MIN_DIFF_TEXT_COLOR)
    _record(result, "TC-08-02", "PASS" if detected else "FAIL")
    assert not result.dimension_mismatch, result.message
    assert not result.matched, f"Expected visual diff, got match: {result.message}"
    assert result.diff_percent >= MIN_DIFF_TEXT_COLOR, result.message
    assert result.diff_mask_path and Path(result.diff_mask_path).is_file()
    assert result.overlay_path and Path(result.overlay_path).is_file()


@pytest.mark.kt08
def test_layout_shift_detected(visual_driver, visual_wait, fixture_url):
    """Сдвиг layout обнаруживается (без auto-resize)."""
    baseline = BASELINES / "home_baseline.png"
    _open_fixture(visual_driver, visual_wait, fixture_url, "kt08", "home_layout_shift.html")
    actual = _capture(visual_driver, "03_layout_shift_actual")

    result = compare_images(
        baseline,
        actual,
        color_tolerance=COLOR_TOLERANCE,
        threshold_percent=MATCH_THRESHOLD_PERCENT,
        artifacts_dir=ARTIFACTS,
        name="03_layout_shift",
    )
    detected = (not result.matched) and (result.diff_percent >= MIN_DIFF_LAYOUT)
    _record(result, "TC-08-03", "PASS" if detected else "FAIL")
    assert not result.dimension_mismatch, result.message
    assert not result.matched, result.message
    assert result.diff_percent >= MIN_DIFF_LAYOUT, result.message


@pytest.mark.kt08
def test_significant_difference_reported_with_metrics(
    visual_driver, visual_wait, fixture_url
):
    """Значительное отличие даёт высокий diff% и диагностические артефакты."""
    baseline = BASELINES / "home_baseline.png"
    _open_fixture(visual_driver, visual_wait, fixture_url, "kt08", "home_significant.html")
    actual = _capture(visual_driver, "04_significant_actual")

    result = compare_images(
        baseline,
        actual,
        color_tolerance=COLOR_TOLERANCE,
        threshold_percent=MATCH_THRESHOLD_PERCENT,
        artifacts_dir=ARTIFACTS,
        name="04_significant",
    )
    detected = (not result.matched) and (result.diff_percent >= MIN_DIFF_SIGNIFICANT)
    _record(result, "TC-08-04", "PASS" if detected else "FAIL")
    assert not result.matched, result.message
    assert result.diff_percent >= MIN_DIFF_SIGNIFICANT, result.message
    assert result.changed_pixels > 0
    assert "DIFF_DETECTED" in result.message
    assert result.overlay_path and Path(result.overlay_path).is_file()


@pytest.mark.kt08
def test_dimension_mismatch_detected(visual_driver, visual_wait, fixture_url):
    """Разные размеры скриншотов обнаруживаются без авто-масштабирования."""
    baseline = BASELINES / "home_baseline.png"
    # Capture same fixture at a smaller window → different PNG dimensions
    visual_driver.set_window_size(900, 700)

    _open_fixture(visual_driver, visual_wait, fixture_url, "kt08", "home.html")
    actual = _capture(visual_driver, "05_dimension_mismatch_actual")

    result = compare_images(
        baseline,
        actual,
        color_tolerance=COLOR_TOLERANCE,
        threshold_percent=MATCH_THRESHOLD_PERCENT,
        artifacts_dir=ARTIFACTS,
        name="05_dimensions",
    )
    ok = result.dimension_mismatch and (not result.matched)
    _record(result, "TC-08-05", "PASS" if ok else "FAIL")
    assert result.dimension_mismatch, result.message
    assert not result.matched, result.message
    assert "DIMENSION_MISMATCH" in result.message
    assert result.baseline_size != result.actual_size
