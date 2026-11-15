"""Inventory and product catalog scenarios from the SauceDemo test plan."""

from decimal import Decimal

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_inventory_products_render_with_details_and_images(
    inventory_page: InventoryPage,
) -> None:
    """TC_INV_01: Every product has complete details and a loaded image."""
    products = inventory_page.get_products()

    assert products
    assert all(product.name.strip() for product in products)
    assert all(product.description.strip() for product in products)
    assert all(product.price > Decimal("0") for product in products)
    assert all(product.image_loaded for product in products)


@pytest.mark.parametrize(
    ("sort_option", "reverse"),
    [("az", False), ("za", True)],
    ids=("name-a-to-z", "name-z-to-a"),
)
def test_products_sort_by_name(
    inventory_page: InventoryPage, sort_option: str, reverse: bool
) -> None:
    """TC_INV_02: Product names sort in either alphabetical direction."""
    inventory_page.sort_products(sort_option)
    product_names = inventory_page.get_product_names()

    assert product_names == sorted(product_names, reverse=reverse)


@pytest.mark.parametrize(
    ("sort_option", "reverse"),
    [("lohi", False), ("hilo", True)],
    ids=("price-low-to-high", "price-high-to-low"),
)
def test_products_sort_by_price(
    inventory_page: InventoryPage, sort_option: str, reverse: bool
) -> None:
    """TC_INV_03: Product prices sort in either numerical direction."""
    inventory_page.sort_products(sort_option)
    prices = inventory_page.get_product_prices()

    assert prices == sorted(prices, reverse=reverse)


@pytest.mark.smoke
def test_add_product_updates_action_and_cart_badge(
    driver: WebDriver, inventory_page: InventoryPage
) -> None:
    """TC_INV_04: Adding a product changes its action and increments the badge."""
    inventory_page.add_product_to_cart("Sauce Labs Backpack")

    assert inventory_page.get_product_action_text("Sauce Labs Backpack") == "Remove"
    assert inventory_page.get_cart_badge_count() == "1"
