"""Page objects for SauceDemo checkout screens."""

from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage, Locator


class CheckoutPage(BasePage):
    """Customer information form and its validation behavior."""

    FIRST_NAME: Locator = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME: Locator = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE: Locator = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON: Locator = (By.CSS_SELECTOR, "[data-test='continue']")
    ERROR_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the checkout form page object."""
        super().__init__(driver, timeout)

    def submit_customer_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        """Fill and submit checkout customer information."""
        self.enter_text(self.FIRST_NAME, first_name)
        self.enter_text(self.LAST_NAME, last_name)
        self.enter_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        """Return the visible checkout validation error."""
        return self.get_text(self.ERROR_MESSAGE)


class CheckoutOverviewPage(BasePage):
    """Order overview details and order completion action."""

    SUBTOTAL: Locator = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX: Locator = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL: Locator = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH_BUTTON: Locator = (By.CSS_SELECTOR, "[data-test='finish']")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the checkout overview page object."""
        super().__init__(driver, timeout)

    @staticmethod
    def _amount(text: str) -> Decimal:
        """Extract a currency amount from a checkout summary label."""
        return Decimal(text.rsplit("$", 1)[-1].strip())

    def get_subtotal(self) -> Decimal:
        """Return the order subtotal."""
        return self._amount(self.get_text(self.SUBTOTAL))

    def get_tax(self) -> Decimal:
        """Return the order tax."""
        return self._amount(self.get_text(self.TAX))

    def get_total(self) -> Decimal:
        """Return the order total."""
        return self._amount(self.get_text(self.TOTAL))

    def finish_order(self) -> None:
        """Submit the order."""
        self.click(self.FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    """Order confirmation page."""

    COMPLETE_HEADER: Locator = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the order confirmation page object."""
        super().__init__(driver, timeout)

    def get_confirmation_message(self) -> str:
        """Return the order confirmation heading."""
        return self.get_text(self.COMPLETE_HEADER)
