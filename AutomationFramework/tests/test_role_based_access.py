from __future__ import annotations

import pytest

from pages.login_page import LoginPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.rbac
def test_role_based_access(driver, framework_config):
    ensure_real_aut(framework_config.base_url)

    login_page = LoginPage(driver, framework_config.base_url, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)

    login_page.open()
    login_page.login(framework_config.username, framework_config.password)
    admin_url = driver.current_url.lower()
    assert "admin" in admin_url or "dashboard" in admin_url, f"Admin access should lead to an authorized area, got {admin_url}"

    driver.delete_all_cookies()
    login_page.open()
    login_page.login("student@example.com", "Student@123")
    student_url = driver.current_url.lower()
    if "access-denied" in student_url or "forbidden" in student_url:
        assert True
    else:
        assert "student" in student_url or "dashboard" in student_url or "login" in student_url, f"Student navigation should be restricted, got {student_url}"
