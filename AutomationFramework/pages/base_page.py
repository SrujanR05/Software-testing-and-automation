from __future__ import annotations

from pathlib import Path
from typing import Any

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.ui import Select

from utils.logger import get_logger
from utils.screenshot_helper import ScreenshotHelper
from utils.wait_helper import WaitHelper


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 20, screenshot_dir: str | Path = "screenshots") -> None:
        self.driver = driver
        self.wait = WaitHelper(driver, timeout=timeout)
        self.logger = get_logger(self.__class__.__name__)
        self.screenshot_dir = screenshot_dir

    def open(self, url: str) -> None:
        self.logger.info("Opening URL: %s", url)
        self.driver.get(url)

    def wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        self.logger.debug("Waiting for element: %s", locator)
        return self.wait.visible(locator)

    def find_elements(self, locator: tuple[str, str]) -> list[WebElement]:
        return self.wait.present_all(locator)

    def click(self, locator: tuple[str, str]) -> WebElement:
        element = self.wait.clickable(locator)
        self.logger.debug("Clicking element: %s", locator)
        element.click()
        return element

    def javascript_click(self, locator: tuple[str, str]) -> None:
        element = self.wait.visible(locator)
        self.logger.debug("JavaScript clicking element: %s", locator)
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator: tuple[str, str], text: str, clear: bool = True) -> WebElement:
        element = self.wait.visible(locator)
        if clear:
            element.clear()
        self.logger.debug("Typing text into element: %s", locator)
        element.send_keys(text)
        return element

    def get_text(self, locator: tuple[str, str]) -> str:
        text = self.wait.visible(locator).text.strip()
        self.logger.debug("Text from %s: %s", locator, text)
        return text

    def get_attribute(self, locator: tuple[str, str], attribute_name: str) -> str | None:
        return self.wait.visible(locator).get_attribute(attribute_name)

    def scroll_to_element(self, locator: tuple[str, str]) -> None:
        element = self.wait.present(locator)
        self.logger.debug("Scrolling to element: %s", locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def take_screenshot(self, name: str = "page") -> str:
        return ScreenshotHelper.capture(self.driver, self.screenshot_dir, name)

    def select_dropdown_by_visible_text(self, locator: tuple[str, str], text: str) -> None:
        select = Select(self.wait.visible(locator))
        select.select_by_visible_text(text)

    def select_dropdown_by_value(self, locator: tuple[str, str], value: str) -> None:
        select = Select(self.wait.visible(locator))
        select.select_by_value(value)

    def select_dropdown_by_index(self, locator: tuple[str, str], index: int) -> None:
        select = Select(self.wait.visible(locator))
        select.select_by_index(index)

    def accept_alert(self) -> str:
        alert = self._wait_for_alert()
        text = alert.text
        alert.accept()
        return text

    def dismiss_alert(self) -> str:
        alert = self._wait_for_alert()
        text = alert.text
        alert.dismiss()
        return text

    def send_text_to_alert(self, text: str) -> None:
        alert = self._wait_for_alert()
        alert.send_keys(text)

    def get_alert_text(self) -> str:
        return self._wait_for_alert().text

    def hover(self, locator: tuple[str, str]) -> None:
        element = self.wait.visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def _wait_for_alert(self) -> Alert:
        return self.wait.alert()
