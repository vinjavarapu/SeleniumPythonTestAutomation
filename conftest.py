"""Shared pytest options, browser lifecycle, and test fixtures."""

import hashlib
import os
import re
import sys
import warnings
from collections.abc import Iterator
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from settings import AppSettings

DEFAULT_BASE_URL = "https://www.saucedemo.com"


def _environment_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise pytest.UsageError(f"{name} must be a boolean value (true/false, yes/no, 1/0, or on/off).")


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register runtime options with environment-variable defaults."""
    group = parser.getgroup("browser")
    group.addoption(
        "--browser",
        choices=("chrome", "firefox"),
        default=os.getenv("SAUCEDEMO_BROWSER", "chrome").lower(),
        help="Browser to use (default: SAUCEDEMO_BROWSER or chrome).",
    )
    group.addoption(
        "--headless",
        action="store_true",
        dest="headless",
        default=_environment_flag("SAUCEDEMO_HEADLESS", True),
        help="Run the browser without a visible window.",
    )
    group.addoption(
        "--headed",
        action="store_false",
        dest="headless",
        help="Run the browser with a visible window.",
    )
    group.addoption(
        "--base-url",
        default=os.getenv("SAUCEDEMO_BASE_URL", DEFAULT_BASE_URL),
        help="SauceDemo base URL (default: SAUCEDEMO_BASE_URL or the public site).",
    )
    group.addoption(
        "--wait-seconds",
        type=float,
        default=float(os.getenv("SAUCEDEMO_WAIT_SECONDS", "10")),
        help="Explicit Selenium wait timeout in seconds.",
    )


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> AppSettings:
    """Build validated, immutable runtime settings."""
    base_url = str(pytestconfig.getoption("--base-url")).rstrip("/")
    wait_seconds = float(pytestconfig.getoption("--wait-seconds"))
    if not base_url.startswith(("http://", "https://")):
        raise pytest.UsageError("--base-url must begin with http:// or https://.")
    if wait_seconds <= 0:
        raise pytest.UsageError("--wait-seconds must be greater than zero.")

    return AppSettings(
        base_url=base_url,
        username=os.getenv("SAUCEDEMO_USERNAME", "standard_user"),
        password=os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce"),
        wait_seconds=wait_seconds,
    )


@pytest.fixture
def driver(
    request: pytest.FixtureRequest,
) -> Iterator[WebDriver]:
    """Create an isolated browser session for each test."""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        if sys.platform.startswith("linux"):
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.headless = headless
        browser = webdriver.Firefox(options=options)

    try:
        browser.set_window_size(1920, 1080)
        browser.implicitly_wait(0)
        request.node.webdriver = browser  # type: ignore[attr-defined]
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def inventory_page(driver: WebDriver, settings: AppSettings) -> InventoryPage:
    """Return the inventory page after signing in as the configured user."""
    login_page = LoginPage(driver, timeout=settings.wait_seconds)
    login_page.open(settings.base_url)
    login_page.login_as_user(settings.username, settings.password)
    return InventoryPage(driver, timeout=settings.wait_seconds)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> Iterator[None]:
    """Save a screenshot for a failed test call without masking its failure."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    browser = getattr(item, "webdriver", None)
    if browser is None:
        return

    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid).strip("_")[:120]
    suffix = hashlib.sha1(item.nodeid.encode("utf-8")).hexdigest()[:8]
    screenshot_path = Path("test-results") / "screenshots" / f"{safe_name}-{suffix}.png"
    try:
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        browser.save_screenshot(str(screenshot_path))
        report.sections.append(("Screenshot", str(screenshot_path.resolve())))
    except (OSError, WebDriverException) as exc:
        warnings.warn(
            f"Could not save failure screenshot for {item.nodeid}: {exc}",
            pytest.PytestWarning,
            stacklevel=1,
        )
