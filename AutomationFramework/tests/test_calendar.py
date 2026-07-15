from __future__ import annotations

import pytest

from pages.calendar_page import CalendarPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.calendar
def test_calendar_validation(driver, framework_config, test_data):
    ensure_real_aut(framework_config.base_url)

    calendar_page = CalendarPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    calendar_page.open(framework_config.base_url)
    future_date = calendar_page.select_future_date(test_data["calendar"]["future_days_ahead"])

    assert future_date, "Future date should be selected"
    assert "-" in future_date, "Future date should be returned in ISO-like format"

    assert calendar_page.is_past_date_rejected(test_data["calendar"]["past_days_behind"]), "Past date should be rejected"
