import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_webdriver_headless() -> None:
    """Setup the webdriver to not be headless if tests are running in a local dev environment."""
    from os import environ

    from brlaw_mcp_server.scraper.webdriver import WebDriver

    WebDriver.headless = "CI" in environ
    print(f"Browsers will be {'visible' if WebDriver.headless else 'headless'}")
