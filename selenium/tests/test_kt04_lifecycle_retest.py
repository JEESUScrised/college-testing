"""KT04 lifecycle retest against FIXED Campus Portal copy (kt04_lifecycle).

Historical seeded FAIL suite in test_kt04_defects.py is preserved unchanged.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pages.campus_portal_pages import DashboardPage, LoginPage, RegisterPage

SHOTS = Path(__file__).resolve().parents[2] / "screenshots" / "kt04" / "lifecycle"


class LifecycleLoginPage(LoginPage):
    PATH = ("kt04_lifecycle", "index.html")


class LifecycleRegisterPage(RegisterPage):
    PATH = ("kt04_lifecycle", "register.html")


class LifecycleDashboardPage(DashboardPage):
    pass


@pytest.mark.kt04
@pytest.mark.kt04_lifecycle
def test_lifecycle_empty_password_rejected(driver, fixture_url):
    login = LifecycleLoginPage(driver).open_fixture(fixture_url)
    login.login("student", "")
    SHOTS.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SHOTS / "retest_seed001_empty_password.png"))
    assert "Вход" in login.title
    assert login.error_visible() is True


@pytest.mark.kt04
@pytest.mark.kt04_lifecycle
def test_lifecycle_invalid_email_rejected(driver, fixture_url):
    page = LifecycleRegisterPage(driver).open_fixture(fixture_url)
    page.register("Иван", "user@mail", "secret123")
    SHOTS.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SHOTS / "retest_seed002_invalid_email.png"))
    assert page.error_visible() is True
    assert page.success_visible() is False


@pytest.mark.kt04
@pytest.mark.kt04_lifecycle
def test_lifecycle_zero_quantity_rejected(driver, fixture_url):
    login = LifecycleLoginPage(driver).open_fixture(fixture_url)
    login.login("student", "student123")
    dash = LifecycleDashboardPage(driver).wait_loaded()
    dash.place_order("0")
    SHOTS.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SHOTS / "retest_seed003_zero_quantity.png"))
    assert dash.error_visible() is True
    assert dash.success_visible() is False
