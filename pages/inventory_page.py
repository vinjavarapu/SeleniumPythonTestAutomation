"""Page object for the SauceDemo inventory screen."""

from dataclasses import dataclass
from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, Locator


@dataclass(frozen=True)
class InventoryProduct:
    """Product details visible in an inventory card."""

    name: str
    description: str
    price: Decimal
    image_loaded: bool


class InventoryPage(BasePage):
    """Inventory locators and product/cart business actions."""

    PAGE_TITLE: Locator = (By.CSS_SELECTOR, "[data-test='title']")
    INVENTORY_ITEMS: Locator = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    PRODUCT_NAME: Locator = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRODUCT_DESCRIPTION: Locator = (
        By.CSS_SELECTOR,
        "[data-test='inventory-item-desc']",
    )
    PRODUCT_PRICE: Locator = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    PRODUCT_IMAGE: Locator = (By.CSS_SELECTOR, ".inventory_item_img img")
    PRODUCT_SORT: Locator = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    SHOPPING_CART_BADGE: Locator = (
        By.CSS_SELECTOR,
        "[data-test='shopping-cart-badge']",
    )
    SHOPPING_CART_LINK: Locator = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the inventory page object."""
        super().__init__(driver, timeout)

    @staticmethod
    def _product_slug(product_name: str) -> str:
        """Convert a displayed product name to SauceDemo's data-test slug."""
        return "-".join(product_name.strip().lower().split())

    @staticmethod
    def _price_value(price_text: str) -> Decimal:
        """Parse a displayed currency value without floating-point rounding."""
        return Decimal(price_text.replace("$", "").strip())

    def add_product_to_cart(self, product_name: str) -> None:
        """Add a named inventory product to the cart."""
        locator: Locator = (
            By.CSS_SELECTOR,
            f"[data-test='add-to-cart-{self._product_slug(product_name)}']",
        )
        self.click(locator)

    def remove_product_from_cart(self, product_name: str) -> None:
        """Remove a named product from the inventory listing."""
        locator: Locator = (
            By.CSS_SELECTOR,
            f"[data-test='remove-{self._product_slug(product_name)}']",
        )
        self.click(locator)

    def get_product_action_text(self, product_name: str) -> str:
        """Return the action button text for a named product."""
        slug = self._product_slug(product_name)
        locator: Locator = (
            By.CSS_SELECTOR,
            f"[data-test='add-to-cart-{slug}'], [data-test='remove-{slug}']",
        )
        return self.get_text(locator)

    def get_products(self) -> list[InventoryProduct]:
        """Return inventory product details and image-load status."""
        cards = self.wait_until_all_present(self.INVENTORY_ITEMS)
        products: list[InventoryProduct] = []
        for card in cards:
            name = card.find_element(*self.PRODUCT_NAME).text
            description = card.find_element(*self.PRODUCT_DESCRIPTION).text
            price_text = card.find_element(*self.PRODUCT_PRICE).text
            image = card.find_element(*self.PRODUCT_IMAGE)
            image_loaded = bool(
                self.driver.execute_script(
                    "return arguments[0].complete && arguments[0].naturalWidth > 0;",
                    image,
                )
            )
            products.append(
                InventoryProduct(
                    name=name,
                    description=description,
                    price=self._price_value(price_text),
                    image_loaded=image_loaded,
                )
            )
        return products

    def get_product_names(self) -> list[str]:
        """Return product names in their currently displayed order."""
        return [product.name for product in self.get_products()]

    def get_product_prices(self) -> list[Decimal]:
        """Return prices in their currently displayed order."""
        return [product.price for product in self.get_products()]

    def sort_products(self, option: str) -> None:
        """Sort products using a SauceDemo sort option (az, za, lohi, hilo)."""
        Select(self.wait_until_visible(self.PRODUCT_SORT)).select_by_value(option)

    def get_page_header(self) -> str:
        """Return the inventory page heading."""
        return self.get_text(self.PAGE_TITLE)

    def get_cart_badge_count(self) -> str:
        """Wait for and return the shopping cart badge count."""
        return self.get_text(self.SHOPPING_CART_BADGE)

    def open_cart(self) -> None:
        """Open the shopping cart."""
        self.click(self.SHOPPING_CART_LINK)
