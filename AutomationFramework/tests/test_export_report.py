from __future__ import annotations

import pytest

from pages.login_page import LoginPage
from pages.report_page import ReportPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.export
def test_export_report(driver, framework_config, test_data):
    ensure_real_aut(framework_config.base_url)

    login_page = LoginPage(driver, framework_config.base_url, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    login_page.open()
    login_page.login(framework_config.username, framework_config.password)

    report_page = ReportPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    report_page.export_report()

    ui_records = report_page.get_ui_records()
    excel_records = report_page.load_exported_excel(framework_config.download_dir)
    mismatches = report_page.compare_records(ui_records, excel_records)

    assert not mismatches, "Excel export should match the UI table data"
