"""Page object for the SauceDemo login screen."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage, Locator


class LoginPage(BasePage):
    """Login page locators and user-facing login actions."""

    USERNAME_INPUT: Locator = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON: Locator = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-test='error']")
    MENU_BUTTON: Locator = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK: Locator = (By.ID, "logout_sidebar_link")

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        """Initialize the login page object."""
        super().__init__(driver, timeout)

    def open(self, base_url: str) -> None:
        """Navigate to the SauceDemo login page."""
        self.driver.get(base_url)

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

    def get_error_message(self) -> str:
        """Return the visible login validation or authentication error."""
        return self.get_text(self.ERROR_MESSAGE)

    def logout(self) -> None:
        """Open the side menu and log out."""
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        self.wait_until_visible(self.LOGIN_BUTTON)
