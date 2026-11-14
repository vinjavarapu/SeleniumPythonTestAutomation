"""Page object for the Sauce Demo login screen."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page locators and user-facing login actions."""

    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the login page object."""
        super().__init__(driver, timeout)

    def enter_username(self, username: str) -> None:
        """Fill the username field."""
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Fill the password field."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """Submit the login form."""
        self.click(self.LOGIN_BUTTON)

    def login_as_user(self, username: str, password: str) -> None:
        """Log in with the supplied credentials."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
