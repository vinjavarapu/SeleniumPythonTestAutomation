"""Page object for the Sauce Demo inventory screen."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage, Locator


class InventoryPage(BasePage):
    """Inventory locators and product/cart business actions."""

    PAGE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    INVENTORY_CONTAINER = (By.CSS_SELECTOR, "[data-test='inventory-container']")
    SHOPPING_CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the inventory page object."""
        super().__init__(driver, timeout)

    @staticmethod
    def _product_slug(product_name: str) -> str:
        """Convert a displayed product name to Sauce Demo's data-test slug."""
        return product_name.lower().replace(" ", "-")

    def add_product_to_cart(self, product_name: str) -> None:
        """Add a named inventory product to the cart."""
        locator: Locator = (
            By.CSS_SELECTOR,
            f"[data-test='add-to-cart-{self._product_slug(product_name)}']",
        )
        self.click(locator)

    def get_page_header(self) -> str:
        """Return the inventory page heading."""
        return self.get_text(self.PAGE_TITLE)

    def get_cart_badge_count(self) -> str:
        """Wait for and return the shopping cart badge count."""
        return self.get_text(self.SHOPPING_CART_BADGE)

    def open_cart(self) -> None:
        """Open the shopping cart using its header container."""
        self.click(self.SHOPPING_CART_LINK)
