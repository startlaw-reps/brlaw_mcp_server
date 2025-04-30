"""Tests for the scraper package.

Besides correctness, these tests must enforce services levels such as maximum response time."""

from typing import TYPE_CHECKING, Final

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from brlaw_mcp_server.scraper.webdriver import WebDriver


MAXIMUM_SCRAPING_TIME: Final[int] = 30


@pytest.fixture
def webdriver() -> "Generator[WebDriver, None, None]":
    from brlaw_mcp_server.scraper.webdriver import WebDriver

    with WebDriver() as wd:
        yield wd


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("criteria", "max_results_len"),
    [
        pytest.param(
            "asdjnaskjdnaajhsbajkhsdjkabsndk12931092381902098",  # Bogus criteria
            1,
            id="no_results",
        ),
        pytest.param(
            "fraude execução",  # Criteria known to return results.
            10,
            id="has_results",
        ),
    ],
)
async def test_scraper_legal_precedents(
    webdriver: "WebDriver",
    criteria: str,
    max_results_len: int,
) -> None:
    """Test behavior when no results are found."""
    import asyncio

    from mcp.types import TextContent

    import brlaw_mcp_server.scraper.core as scraper

    async with asyncio.timeout(MAXIMUM_SCRAPING_TIME):
        results = await scraper.scrape_legal_precedents(webdriver, criteria, "STJ")

    assert max_results_len >= len(results) >= 1
    assert isinstance(results[0], TextContent)
    assert (
        (results[0].text == scraper.NO_RESULTS_MESSAGE)
        if max_results_len == 1
        else (results[0].text != scraper.NO_RESULTS_MESSAGE)
    )
