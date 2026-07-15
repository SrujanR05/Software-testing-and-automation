from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class DashboardPage(BasePage):
    RECORD_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    RECORD_CELLS = (By.CSS_SELECTOR, "table tbody tr td")
    SORTABLE_HEADER = (By.CSS_SELECTOR, "th[data-test='sortable-column'], th.sortable")
    PAGE_LINKS = (By.CSS_SELECTOR, "nav[aria-label='Pagination'] button, nav[aria-label='Pagination'] a")
    SORTABLE_CELLS = (By.CSS_SELECTOR, "table tbody tr td:nth-child(2)")
    SESSION_EXPIRED_MESSAGE = (By.CSS_SELECTOR, ".session-expired, [data-test='session-expired']")
    HYPERLINKS = (By.CSS_SELECTOR, "a[href]")

    def __init__(self, driver: WebDriver, timeout: int = 20, screenshot_dir: str = "screenshots") -> None:
        super().__init__(driver, timeout=timeout, screenshot_dir=screenshot_dir)

    def get_row_texts(self) -> list[str]:
        return [row.text.strip() for row in self.find_elements(self.RECORD_ROWS)]

    def get_record_values(self, column_index: int = 0) -> list[str]:
        values: list[str] = []
        for row in self.find_elements(self.RECORD_ROWS):
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            if column_index < len(cells):
                values.append(cells[column_index].text.strip())
        return values

    def sort_by_column(self) -> None:
        self.click(self.SORTABLE_HEADER)

    def is_records_per_page(self, expected_count: int = 10) -> bool:
        return len(self.find_elements(self.RECORD_ROWS)) == expected_count

    def get_page_numbers(self) -> list[str]:
        numbers = []
        for element in self.find_elements(self.PAGE_LINKS):
            text = element.text.strip()
            if text:
                numbers.append(text)
        return numbers

    def go_to_page(self, page_number: int) -> None:
        locator = (By.XPATH, f"//button[normalize-space()='{page_number}'] | //a[normalize-space()='{page_number}']")
        self.click(locator)

    @staticmethod
    def is_sorted_ascending(values: list[str]) -> bool:
        return values == sorted(values)

    @staticmethod
    def is_sorted_descending(values: list[str]) -> bool:
        return values == sorted(values, reverse=True)

    @staticmethod
    def compare_lists(actual: list[str], expected: list[str]) -> bool:
        return actual == expected

    def collect_hyperlinks(self) -> list[str]:
        return [element.get_attribute("href") or "" for element in self.find_elements(self.HYPERLINKS)]

    def wait_for_session_expired_message(self) -> str:
        return self.get_text(self.SESSION_EXPIRED_MESSAGE)
