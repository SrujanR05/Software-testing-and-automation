from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.api
@pytest.mark.ui
def test_api_validation(driver, framework_config, api_helper):
    ensure_real_aut(framework_config.base_url, framework_config.api_base_url)

    response = api_helper.get("/students")
    assert response.status_code == 200, f"Expected API status 200, got {response.status_code}"

    api_payload = api_helper.parse_json(response)
    assert api_payload, "API should return at least one record"

    login_page = LoginPage(driver, framework_config.base_url, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    login_page.open()
    login_page.login(framework_config.username, framework_config.password)

    dashboard_page = DashboardPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    ui_rows = dashboard_page.get_row_texts()
    assert ui_rows, "UI should return at least one row"

    first_api_row = api_payload[0]
    first_api_name = str(first_api_row.get("name", "")).strip()
    assert any(first_api_name in row for row in ui_rows), "API name should be visible in the UI data"
