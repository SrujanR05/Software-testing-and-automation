from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class LinksPage(BasePage):
    LINK_ELEMENTS = (By.CSS_SELECTOR, "a[href]")

    def __init__(self, driver: WebDriver, timeout: int = 20, screenshot_dir: str = "screenshots") -> None:
        super().__init__(driver, timeout=timeout, screenshot_dir=screenshot_dir)

    def collect_links(self) -> list[str]:
        links: list[str] = []
        for element in self.find_elements(self.LINK_ELEMENTS):
            href = element.get_attribute("href")
            if href:
                links.append(href)
        return links
