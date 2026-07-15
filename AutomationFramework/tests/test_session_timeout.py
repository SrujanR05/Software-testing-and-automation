from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.session_timeout
def test_session_timeout(driver, framework_config):
    ensure_real_aut(framework_config.base_url)

    login_page = LoginPage(driver, framework_config.base_url, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    login_page.open()
    login_page.login(framework_config.username, framework_config.password)

    driver.delete_all_cookies()
    driver.refresh()

    if "login" in driver.current_url.lower():
        assert "login" in driver.current_url.lower(), "Session timeout should redirect the user to the login page"
    else:
        dashboard_page = DashboardPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
        message = dashboard_page.wait_for_session_expired_message().lower()
        assert "session" in message and ("expired" in message or "timeout" in message), "Expected a visible session-expired message"
