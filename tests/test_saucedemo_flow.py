"""Cart and checkout flows specified in the SauceDemo test plan."""

from decimal import Decimal

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutOverviewPage,
    CheckoutPage,
)
from pages.inventory_page import InventoryPage
from settings import AppSettings

BACKPACK = "Sauce Labs Backpack"


@pytest.mark.smoke
def test_inventory_item_persists_in_cart(
    driver: WebDriver, inventory_page: InventoryPage, settings: AppSettings
) -> None:
    """TC_CART_01: Added product details and quantity persist in the cart."""
    inventory_page.add_product_to_cart(BACKPACK)
    inventory_page.open_cart()

    cart_page = CartPage(driver, timeout=settings.wait_seconds)
    details = cart_page.get_item_details(BACKPACK)
    assert details == {
        "name": BACKPACK,
        "description": (
            "carry.allTheThings() with the sleek, streamlined Sly Pack that "
            "melds uncompromising style with unequaled laptop and tablet "
            "protection."
        ),
        "price": Decimal("29.99"),
        "quantity": "1",
    }


def test_remove_item_from_cart_decrements_badge(
    driver: WebDriver, inventory_page: InventoryPage, settings: AppSettings
) -> None:
    """TC_CART_02: Removing an item decreases the cart badge count."""
    inventory_page.add_product_to_cart(BACKPACK)
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")
    inventory_page.open_cart()

    cart_page = CartPage(driver, timeout=settings.wait_seconds)
    assert cart_page.get_badge_count() == "2"
    cart_page.remove_item(BACKPACK)

    assert cart_page.get_badge_count() == "1"
    assert cart_page.get_item_names() == ["Sauce Labs Bike Light"]


@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "expected_error"),
    [
        ("", "Tester", "12345", "Error: First Name is required"),
        ("Ravi", "", "12345", "Error: Last Name is required"),
        ("Ravi", "Tester", "", "Error: Postal Code is required"),
    ],
    ids=("missing-first-name", "missing-last-name", "missing-postal-code"),
)
def test_checkout_requires_customer_information(
    driver: WebDriver,
    inventory_page: InventoryPage,
    settings: AppSettings,
    first_name: str,
    last_name: str,
    postal_code: str,
    expected_error: str,
) -> None:
    """TC_CHK_01: Checkout reports the specific missing required field."""
    inventory_page.add_product_to_cart(BACKPACK)
    inventory_page.open_cart()
    CartPage(driver, timeout=settings.wait_seconds).checkout()

    checkout_page = CheckoutPage(driver, timeout=settings.wait_seconds)
    checkout_page.submit_customer_information(first_name, last_name, postal_code)

    assert checkout_page.get_error_message() == expected_error


@pytest.mark.smoke
def test_complete_checkout_shows_correct_totals_and_confirmation(
    driver: WebDriver,
    inventory_page: InventoryPage,
    settings: AppSettings,
) -> None:
    """TC_CHK_02: Complete checkout and verify calculated totals and confirmation."""
    inventory_page.add_product_to_cart(BACKPACK)
    inventory_page.open_cart()
    CartPage(driver, timeout=settings.wait_seconds).checkout()

    checkout_page = CheckoutPage(driver, timeout=settings.wait_seconds)
    checkout_page.submit_customer_information("Ravi", "Tester", "12345")

    overview = CheckoutOverviewPage(driver, timeout=settings.wait_seconds)
    assert overview.get_subtotal() == Decimal("29.99")
    assert overview.get_tax() > Decimal("0")
    assert overview.get_total() == overview.get_subtotal() + overview.get_tax()

    overview.finish_order()
    complete_page = CheckoutCompletePage(driver, timeout=settings.wait_seconds)
    assert complete_page.get_confirmation_message().casefold() == ("thank you for your order!")
    assert driver.current_url.endswith("/checkout-complete.html")
    assert settings.base_url in driver.current_url
