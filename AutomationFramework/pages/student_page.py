from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class StudentPage(BasePage):
    STUDENT_ID_INPUT = (By.ID, "studentId")
    STUDENT_NAME_INPUT = (By.ID, "studentName")
    STUDENT_EMAIL_INPUT = (By.ID, "studentEmail")
    ADD_BUTTON = (By.CSS_SELECTOR, "button[data-test='add-student']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[data-test='save-student']")
    DUPLICATE_MESSAGE = (By.CSS_SELECTOR, ".validation-error, [data-test='duplicate-message']")

    def __init__(self, driver: WebDriver, timeout: int = 20, screenshot_dir: str = "screenshots") -> None:
        super().__init__(driver, timeout=timeout, screenshot_dir=screenshot_dir)

    def add_student(self, student_id: str, student_name: str, student_email: str | None = None) -> None:
        self.send_keys(self.STUDENT_ID_INPUT, student_id)
        self.send_keys(self.STUDENT_NAME_INPUT, student_name)
        if student_email:
            self.send_keys(self.STUDENT_EMAIL_INPUT, student_email)
        self.click(self.ADD_BUTTON)
        self.click(self.SAVE_BUTTON)

    def get_duplicate_message(self) -> str:
        return self.get_text(self.DUPLICATE_MESSAGE)
