"""End-to-end tests for key Sauce Demo user flows."""

import os

from selenium.webdriver.remote.webdriver import WebDriver

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BASE_URL = "https://www.saucedemo.com/"
STANDARD_USER = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")


def test_successful_login_and_inventory_load(driver: WebDriver) -> None:
    """Verify a standard user can sign in and reach inventory."""
    driver.get(BASE_URL)
    LoginPage(driver).login_as_user(STANDARD_USER, PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.get_page_header() == "Products"


def test_add_product_to_cart(driver: WebDriver) -> None:
    """Verify adding the Sauce Labs Backpack updates the cart badge."""
    driver.get(BASE_URL)
    LoginPage(driver).login_as_user(STANDARD_USER, PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.get_page_header() == "Products"
    inventory_page.add_product_to_cart("Sauce Labs Backpack")

    assert inventory_page.get_cart_badge_count() == "1"
