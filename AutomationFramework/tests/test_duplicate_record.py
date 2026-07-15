from __future__ import annotations

import pytest

from pages.login_page import LoginPage
from pages.student_page import StudentPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.duplicate
def test_duplicate_record_validation(driver, framework_config, test_data):
    ensure_real_aut(framework_config.base_url)

    login_page = LoginPage(driver, framework_config.base_url, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    login_page.open()
    login_page.login(framework_config.username, framework_config.password)

    student_page = StudentPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    student = test_data["student"]
    student_page.add_student(student["student_id"], student["student_name"])
    student_page.add_student(student["student_id"], student["student_name"])

    message = student_page.get_duplicate_message().lower()
    assert "duplicate" in message or "already exists" in message, f"Expected duplicate validation message, got: {message}"
