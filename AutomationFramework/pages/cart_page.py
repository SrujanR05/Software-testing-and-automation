from __future__ import annotations

import re
from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class CartPage(BasePage):
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[data-test='quantity'], input.qty")
    UPDATE_BUTTON = (By.CSS_SELECTOR, "button[data-test='update-cart'], button.update")
    SUBTOTAL_VALUE = (By.CSS_SELECTOR, "[data-test='subtotal'], .subtotal")
    TAX_VALUE = (By.CSS_SELECTOR, "[data-test='tax'], .tax")
    GRAND_TOTAL_VALUE = (By.CSS_SELECTOR, "[data-test='grand-total'], .grand-total")

    def __init__(self, driver: WebDriver, timeout: int = 20, screenshot_dir: str = "screenshots") -> None:
        super().__init__(driver, timeout=timeout, screenshot_dir=screenshot_dir)

    def update_quantity(self, quantity: int) -> None:
        self.send_keys(self.QUANTITY_INPUT, str(quantity))
        self.click(self.UPDATE_BUTTON)

    def get_amount(self, locator: tuple[str, str]) -> Decimal:
        text = self.get_text(locator)
        cleaned = re.sub(r"[^0-9.]", "", text)
        return Decimal(cleaned or "0")

    def get_subtotal(self) -> Decimal:
        return self.get_amount(self.SUBTOTAL_VALUE)

    def get_tax(self) -> Decimal:
        return self.get_amount(self.TAX_VALUE)

    def get_grand_total(self) -> Decimal:
        return self.get_amount(self.GRAND_TOTAL_VALUE)

    @staticmethod
    def calculate_grand_total(subtotal: Decimal, tax_rate: Decimal) -> Decimal:
        return subtotal + (subtotal * tax_rate)
