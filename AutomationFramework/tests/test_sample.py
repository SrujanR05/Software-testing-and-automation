from __future__ import annotations

from utils.date_utils import DateUtils


def test_framework_smoke(framework_config, test_data):
    assert framework_config.browser.lower() == "chrome"
    assert framework_config.explicit_wait > 0
    assert test_data["pagination"]["expected_records_per_page"] == 10
    assert DateUtils.future_date(1)
