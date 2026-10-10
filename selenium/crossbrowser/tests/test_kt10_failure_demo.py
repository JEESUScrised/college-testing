"""Controlled negative demo: proves screenshot-on-failure hook works.

Run separately from the main matrix. Expected exit code != 0.
"""

from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.kt10_failure_demo
@pytest.mark.parametrize("kt10_browser", ["chrome"], indirect=True)
def test_intentional_failure_for_screenshot_hook(kt10_driver, kt10_wait, kt10_url):
    """Намеренный FAIL для демонстрации screenshot-on-failure (не часть матрицы PASS)."""
    kt10_driver.get(kt10_url("kt10", "home.html"))
    kt10_wait.until(EC.visibility_of_element_located((By.ID, "heading")))
    assert False, "KT10 controlled failure demo: screenshot-on-failure expected"
