"""Shared Selenium interactions for page objects."""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = Tuple[str, str]


class BasePage:
    """Provide explicit-wait wrappers for common browser interactions."""

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the page object with a driver and wait timeout."""
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_visible(self, locator: Locator) -> WebElement:
        """Wait for and return a visible element."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator: Locator) -> WebElement:
        """Wait for and return an element that can be clicked."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Locator) -> None:
        """Click an element after it becomes clickable."""
        self.wait_until_clickable(locator).click()

    def enter_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        """Enter text into a visible field, clearing it by default."""
        element = self.wait_until_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        """Return the text of a visible element."""
        return self.wait_until_visible(locator).text
