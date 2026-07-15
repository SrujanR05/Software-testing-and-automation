from __future__ import annotations

from pathlib import Path
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.excel_reader import ExcelReader
from utils.file_utils import FileDownloadVerifier


class ReportPage(BasePage):
    EXPORT_BUTTON = (By.CSS_SELECTOR, "button[data-test='export-excel'], a[data-test='export-excel']")
    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    TABLE_HEADERS = (By.CSS_SELECTOR, "table thead th")

    def __init__(self, driver: WebDriver, timeout: int = 20, screenshot_dir: str = "screenshots") -> None:
        super().__init__(driver, timeout=timeout, screenshot_dir=screenshot_dir)

    def export_report(self) -> None:
        self.click(self.EXPORT_BUTTON)

    def get_ui_rows(self) -> list[list[str]]:
        rows: list[list[str]] = []
        for row in self.find_elements(self.TABLE_ROWS):
            rows.append([cell.text.strip() for cell in row.find_elements(By.CSS_SELECTOR, "td")])
        return rows

    def get_ui_records(self) -> list[dict[str, str]]:
        headers = [header.text.strip() for header in self.find_elements(self.TABLE_HEADERS)]
        ui_rows = self.get_ui_rows()
        records: list[dict[str, str]] = []
        for row in ui_rows:
            record = {headers[index]: value for index, value in enumerate(row) if index < len(headers)}
            records.append(record)
        return records

    def load_exported_excel(self, download_dir: str | Path, file_name: str | None = None, sheet_name: str | None = None) -> list[dict[str, Any]]:
        downloaded_file = FileDownloadVerifier.wait_for_download(download_dir, file_name)
        return ExcelReader(downloaded_file).read_rows(sheet_name)

    @staticmethod
    def compare_records(ui_records: list[dict[str, Any]], excel_records: list[dict[str, Any]]) -> list[str]:
        mismatches: list[str] = []
        if len(ui_records) != len(excel_records):
            mismatches.append(f"Record count mismatch: UI={len(ui_records)} Excel={len(excel_records)}")
            return mismatches

        for index, (ui_record, excel_record) in enumerate(zip(ui_records, excel_records, strict=False), start=1):
            if ui_record != excel_record:
                mismatches.append(f"Row {index} mismatch: UI={ui_record} Excel={excel_record}")
        return mismatches
