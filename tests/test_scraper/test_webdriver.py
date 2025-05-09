"""Test the webdriver module."""


def test_constructor() -> None:
    """Test if the WebDriver can be instantiated."""
    from brlaw_mcp_server.scraper.webdriver import WebDriver

    with WebDriver() as driver:
        driver.get("https://www.google.com")
        assert isinstance(driver, WebDriver)
