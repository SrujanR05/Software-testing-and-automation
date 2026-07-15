from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.date_utils import DateUtils


class CalendarPage(BasePage):
    DATE_INPUT = (By.CSS_SELECTOR, "input[data-test='date-input'], input[type='date']")
    CALENDAR_WIDGET = (By.CSS_SELECTOR, ".calendar, [role='dialog'][data-test='calendar']")
    NEXT_MONTH_BUTTON = (By.CSS_SELECTOR, "button[aria-label*='Next'], button[data-test='next-month']")
    PREVIOUS_MONTH_BUTTON = (By.CSS_SELECTOR, "button[aria-label*='Previous'], button[data-test='previous-month']")
    DAY_CELLS = (By.CSS_SELECTOR, ".calendar-day, [data-day], td[role='gridcell']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".date-error, [data-test='date-error']")

    def __init__(self, driver: WebDriver, timeout: int = 20, screenshot_dir: str = "screenshots") -> None:
        super().__init__(driver, timeout=timeout, screenshot_dir=screenshot_dir)

    def select_future_date(self, days_ahead: int = 1) -> str:
        target_date = DateUtils.future_date(days_ahead)
        return self.select_date(target_date)

    def select_past_date(self, days_behind: int = 1) -> str:
        target_date = DateUtils.past_date(days_behind)
        return self.select_date(target_date)

    def select_date(self, target_date: str) -> str:
        try:
            self.send_keys(self.DATE_INPUT, target_date)
        except Exception:
            self._set_date_via_javascript(target_date)
        return target_date

    def is_past_date_rejected(self, days_behind: int = 1) -> bool:
        target_date = DateUtils.past_date(days_behind)
        self.select_date(target_date)
        selected_value = self.get_selected_date()
        if selected_value and selected_value != target_date:
            return True

        try:
            message = self.get_error_message().lower()
            return any(keyword in message for keyword in {"past", "invalid", "disabled", "expired"})
        except Exception:
            return False

    def get_selected_date(self) -> str:
        value = self.get_attribute(self.DATE_INPUT, "value")
        return value or ""

    def _set_date_via_javascript(self, target_date: str) -> None:
        element = self.wait_for_element(self.DATE_INPUT)
        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            element,
            target_date,
        )

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
