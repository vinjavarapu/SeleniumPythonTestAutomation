"""Authentication scenarios specified in the SauceDemo test plan."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from settings import AppSettings


@pytest.mark.smoke
def test_standard_user_can_login(driver: WebDriver, settings: AppSettings) -> None:
    """TC_AUTH_01: A valid standard account reaches the inventory page."""
    login_page = LoginPage(driver, timeout=settings.wait_seconds)
    login_page.open(settings.base_url)
    login_page.login_as_user(settings.username, settings.password)

    assert InventoryPage(driver, timeout=settings.wait_seconds).get_page_header() == ("Products")
    assert driver.current_url.endswith("/inventory.html")


@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        (
            "locked_out_user",
            "secret_sauce",
            "Epic sadface: Sorry, this user has been locked out.",
        ),
        (
            "invalid_user",
            "invalid_password",
            "Epic sadface: Username and password do not match any user in this service",
        ),
        ("", "", "Epic sadface: Username is required"),
    ],
    ids=("locked-out-account", "invalid-credentials", "empty-credentials"),
)
def test_login_rejects_invalid_credentials(
    driver: WebDriver,
    settings: AppSettings,
    username: str,
    password: str,
    expected_error: str,
) -> None:
    """TC_AUTH_02-04: Login displays the expected authentication error."""
    login_page = LoginPage(driver, timeout=settings.wait_seconds)
    login_page.open(settings.base_url)
    login_page.login_as_user(username, password)

    assert login_page.get_error_message() == expected_error


@pytest.mark.smoke
def test_user_can_logout_from_side_menu(
    driver: WebDriver, inventory_page: InventoryPage, settings: AppSettings
) -> None:
    """TC_AUTH_05: Logout returns the user to the login page."""
    login_page = LoginPage(driver, timeout=settings.wait_seconds)
    login_page.logout()

    assert driver.current_url.rstrip("/") == settings.base_url
    assert login_page.wait_until_visible(LoginPage.LOGIN_BUTTON).is_displayed()
