"""КТ 04: тест-кейсы Campus Portal Demo (включая выявление seeded-дефектов)."""

from __future__ import annotations

import pytest

from pages.campus_portal_pages import DashboardPage, LoginPage, RegisterPage


@pytest.mark.kt04
def test_tc01_valid_login_passes(driver, fixture_url, save_screenshot):
    """TC-01: валидный вход student/student123 должен открыть кабинет."""
    login = LoginPage(driver).open_fixture(fixture_url)
    login.login("student", "student123")

    dash = DashboardPage(driver).wait_loaded()
    save_screenshot("kt04", "tc01_valid_login")

    assert dash.user_label() == "student"
    assert "Кабинет" in dash.title


@pytest.mark.kt04
def test_tc02_empty_password_should_be_rejected(driver, fixture_url, save_screenshot):
    """TC-02 / SEED-001: пустой пароль должен отклоняться (ожидаемое поведение)."""
    login = LoginPage(driver).open_fixture(fixture_url)
    login.login("student", "")
    save_screenshot("kt04", "tc02_seed001_empty_password")

    # Correct product expectation: stay on login and show an error.
    assert "Вход" in login.title, (
        "SEED-001: вход с пустым паролем не должен открывать кабинет"
    )
    assert login.error_visible() is True


@pytest.mark.kt04
def test_tc03_invalid_email_should_be_rejected(driver, fixture_url, save_screenshot):
    """TC-03 / SEED-002: email без TLD должен отклоняться."""
    page = RegisterPage(driver).open_fixture(fixture_url)
    page.register("Иван", "user@mail", "secret123")
    save_screenshot("kt04", "tc03_seed002_invalid_email")

    assert page.error_visible() is True, (
        "SEED-002: регистрация с email user@mail должна показывать ошибку"
    )
    assert page.success_visible() is False


@pytest.mark.kt04
def test_tc04_zero_quantity_should_be_rejected(driver, fixture_url, save_screenshot):
    """TC-04 / SEED-003: количество 0 должно давать ошибку валидации."""
    login = LoginPage(driver).open_fixture(fixture_url)
    login.login("student", "student123")
    dash = DashboardPage(driver).wait_loaded()
    dash.place_order("0")
    save_screenshot("kt04", "tc04_seed003_zero_quantity")

    assert dash.error_visible() is True, (
        "SEED-003: заказ с количеством 0 должен показывать ошибку"
    )
    assert dash.success_visible() is False


@pytest.mark.kt04
def test_tc05_valid_order_passes(driver, fixture_url, save_screenshot):
    """TC-05: заказ с количеством 2 должен оформляться успешно."""
    login = LoginPage(driver).open_fixture(fixture_url)
    login.login("student", "student123")
    dash = DashboardPage(driver).wait_loaded()
    dash.place_order("2")
    save_screenshot("kt04", "tc05_valid_order")

    assert dash.success_visible() is True
    assert "шт.: 2" in dash.success_text()
