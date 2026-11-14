"""Pytest fixtures for Sauce Demo browser tests."""

from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Create a maximized Chrome session and always close it after the test."""
    options = Options()
    options.add_argument("--headless=new")
    browser = webdriver.Chrome(options=options)
    try:
        browser.maximize_window()
        yield browser
    finally:
        browser.quit()
