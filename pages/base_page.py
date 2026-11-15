"""Shared explicit-wait interactions for page objects."""

from collections.abc import Sequence

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]


class BasePage:
    """Provide explicit-wait wrappers for common browser interactions."""

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the page object with a driver and wait timeout."""
        self.driver = driver
        self.wait = WebDriverWait(
            driver, timeout, ignored_exceptions=(StaleElementReferenceException,)
        )

    def wait_until_visible(self, locator: Locator) -> WebElement:
        """Wait for and return a visible element."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_present(self, locator: Locator) -> WebElement:
        """Wait for and return an element present in the DOM."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_until_clickable(self, locator: Locator) -> WebElement:
        """Wait for and return an element that can be clicked."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_url_contains(self, value: str) -> None:
        """Wait until the current URL contains the expected value."""
        self.wait.until(EC.url_contains(value))

    def click(self, locator: Locator) -> None:
        """Click an element after it becomes clickable."""

        def click_when_ready(_: WebDriver) -> bool:
            element = EC.element_to_be_clickable(locator)(self.driver)
            if not element:
                return False
            element.click()
            return True

        self.wait.until(click_when_ready)

    def enter_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        """Enter text into a visible field, clearing it by default."""
        element = self.wait_until_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        """Return the text of a visible element."""
        return self.wait_until_visible(locator).text

    def find_all(self, locator: Locator) -> Sequence[WebElement]:
        """Return all elements matching a locator."""
        return self.driver.find_elements(*locator)

    def wait_until_all_present(self, locator: Locator) -> list[WebElement]:
        """Wait for and return all elements matching a locator."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
