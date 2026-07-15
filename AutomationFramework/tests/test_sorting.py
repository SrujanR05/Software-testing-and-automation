from __future__ import annotations

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.sorting
def test_sorting_verification(driver, framework_config):
    ensure_real_aut(framework_config.base_url)

    login_page = LoginPage(driver, framework_config.base_url, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    login_page.open()
    login_page.login(framework_config.username, framework_config.password)

    dashboard_page = DashboardPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    dashboard_page.sort_by_column()
    ascending_values = dashboard_page.get_record_values(column_index=1)

    assert ascending_values, "Sortable column should return at least one value"
    assert dashboard_page.is_sorted_ascending(ascending_values), "Ascending order validation failed"

    dashboard_page.sort_by_column()
    descending_values = dashboard_page.get_record_values(column_index=1)

    assert dashboard_page.is_sorted_descending(descending_values), "Descending order validation failed"
    assert dashboard_page.compare_lists(ascending_values, sorted(ascending_values)), "Programmatic ascending comparison failed"
    assert dashboard_page.compare_lists(descending_values, sorted(descending_values, reverse=True)), "Programmatic descending comparison failed"
