from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.pagination
def test_pagination_validation(driver, framework_config, test_data):
    # Debug information
    print("\n================== DEBUG CONFIG ==================")
    print(f"Base URL      : {framework_config.base_url}")
    print(f"API Base URL  : {framework_config.api_base_url}")
    print(f"Username      : {framework_config.username}")
    print(f"Browser       : {framework_config.browser}")
    print(f"Headless      : {framework_config.headless}")
    print("==================================================\n")

    ensure_real_aut(
        framework_config.base_url,
        framework_config.api_base_url,
    )

    login_page = LoginPage(
        driver,
        framework_config.base_url,
        timeout=framework_config.explicit_wait,
        screenshot_dir=framework_config.screenshot_dir,
    )

    login_page.open()
    login_page.login(
        framework_config.username,
        framework_config.password,
    )

    dashboard_page = DashboardPage(
        driver,
        timeout=framework_config.explicit_wait,
        screenshot_dir=framework_config.screenshot_dir,
    )

    expected_records = test_data["pagination"]["expected_records_per_page"]

    first_page_records = dashboard_page.get_row_texts()

    assert len(first_page_records) == expected_records, (
        f"Expected {expected_records} records per page, "
        f"got {len(first_page_records)}"
    )

    assert dashboard_page.is_records_per_page(expected_records), (
        "Pagination should show 10 records per page"
    )

    page_numbers = dashboard_page.get_page_numbers()

    assert page_numbers[0] == "1", (
        f"Expected first page number to be 1, got {page_numbers[0]}"
    )

    if len(page_numbers) > 1:
        dashboard_page.go_to_page(2)
        second_page_records = dashboard_page.get_row_texts()

        assert first_page_records != second_page_records, (
            "Page 1 and Page 2 records should differ"
        )