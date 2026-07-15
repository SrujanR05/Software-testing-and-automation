from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WaitHelper:
    def __init__(self, driver: WebDriver, timeout: int = 20, poll_frequency: float = 0.5) -> None:
        self.driver = driver
        self.timeout = timeout
        self.poll_frequency = poll_frequency

    def visible(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll_frequency).until(
            EC.visibility_of_element_located(locator)
        )

    def clickable(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll_frequency).until(
            EC.element_to_be_clickable(locator)
        )

    def present(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll_frequency).until(
            EC.presence_of_element_located(locator)
        )

    def present_all(self, locator: tuple[str, str]) -> list[WebElement]:
        return WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll_frequency).until(
            EC.presence_of_all_elements_located(locator)
        )

    def invisible(self, locator: tuple[str, str]) -> bool:
        return WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll_frequency).until(
            EC.invisibility_of_element_located(locator)
        )

    def alert(self):
        return WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll_frequency).until(
            EC.alert_is_present()
        )
