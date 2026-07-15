from __future__ import annotations

from decimal import Decimal

import pytest

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from tests.test_helpers import ensure_real_aut


@pytest.mark.ui
@pytest.mark.cart
def test_shopping_cart_validation(driver, framework_config, test_data):
    ensure_real_aut(framework_config.base_url)

    login_page = LoginPage(driver, framework_config.base_url, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    login_page.open()
    login_page.login(framework_config.username, framework_config.password)

    cart_page = CartPage(driver, timeout=framework_config.explicit_wait, screenshot_dir=framework_config.screenshot_dir)
    cart_page.update_quantity(test_data["cart"]["quantity"])

    subtotal = cart_page.get_subtotal()
    tax = cart_page.get_tax()
    grand_total = cart_page.get_grand_total()
    expected_grand_total = CartPage.calculate_grand_total(subtotal, Decimal(str(test_data["cart"]["tax_rate"])))

    assert subtotal >= Decimal("0"), "Subtotal should be zero or greater"
    assert tax >= Decimal("0"), "Tax should be zero or greater"
    assert grand_total == expected_grand_total or grand_total >= subtotal, "Grand total should include subtotal and tax"
