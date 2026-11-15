"""Page object for the SauceDemo shopping cart."""

from decimal import Decimal
from typing import Literal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage, Locator


class CartPage(BasePage):
    """Shopping cart item details and checkout actions."""

    CART_ITEMS: Locator = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_NAME: Locator = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_DESCRIPTION: Locator = (
        By.CSS_SELECTOR,
        "[data-test='inventory-item-desc']",
    )
    ITEM_PRICE: Locator = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    ITEM_QUANTITY: Locator = (By.CSS_SELECTOR, "[data-test='item-quantity']")
    CHECKOUT_BUTTON: Locator = (By.CSS_SELECTOR, "[data-test='checkout']")
    CONTINUE_SHOPPING_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "[data-test='continue-shopping']",
    )
    CART_BADGE: Locator = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the cart page object."""
        super().__init__(driver, timeout)

    def get_item_names(self) -> list[str]:
        """Return names of items currently in the cart."""

        def read_names(_: WebDriver) -> list[str] | Literal[False]:
            items = self.find_all(self.CART_ITEMS)
            if not items:
                return False
            return [item.find_element(*self.ITEM_NAME).text for item in items]

        return self.wait.until(read_names)

    def get_item_details(self, product_name: str) -> dict[str, str | Decimal]:
        """Return the visible details for a named cart item."""

        def read_details(
            _: WebDriver,
        ) -> dict[str, str | Decimal] | Literal[False]:
            for item in self.find_all(self.CART_ITEMS):
                name = item.find_element(*self.ITEM_NAME).text
                if name == product_name:
                    price = item.find_element(*self.ITEM_PRICE).text
                    return {
                        "name": name,
                        "description": item.find_element(*self.ITEM_DESCRIPTION).text,
                        "price": Decimal(price.replace("$", "").strip()),
                        "quantity": item.find_element(*self.ITEM_QUANTITY).text,
                    }
            return False

        return self.wait.until(read_details)

    def remove_item(self, product_name: str) -> None:
        """Remove a named item from the cart."""
        slug = "-".join(product_name.strip().lower().split())
        locator: Locator = (
            By.CSS_SELECTOR,
            f"[data-test='remove-{slug}']",
        )
        self.click(locator)

    def get_badge_count(self) -> str:
        """Return the cart badge count."""
        return self.get_text(self.CART_BADGE)

    def checkout(self) -> None:
        """Proceed to the customer information step."""
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """Return to the inventory listing."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
