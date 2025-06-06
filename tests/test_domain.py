import asyncio
from os import environ

import pytest
from patchright.async_api import async_playwright

from brlaw_mcp_server.domain.stj import StjLegalPrecedent


@pytest.mark.parametrize(
    ("summary", "max_results_len"),
    [
        pytest.param(
            "asdjnaskjdnaajhsbajkhsdjkabsndk12931092381902098",  # Bogus criteria
            0,
            id="no_results",
        ),
        pytest.param(
            "fraude execução",  # Criteria known to return results.
            20,
            id="has_results",
        ),
    ],
)
async def test_research_stj_legal_precedents(
    summary: str,
    max_results_len: int,
) -> None:
    """Test the research method of the STJLegalPrecedent class.

    :param summary: The summary to search for.
    :param max_results_len: The maximum number of results to expect."""

    async with asyncio.timeout(30), async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless="CI" in environ)
        page = await browser.new_page()

        for desired_results_page in range(1, 3):
            precedents = await StjLegalPrecedent.research(
                page,
                summary_search_prompt=summary,
                desired_page=desired_results_page,
            )

            assert max_results_len >= len(precedents) >= 0
            if max_results_len == 0:
                return

            for precedent in precedents:
                assert isinstance(precedent, StjLegalPrecedent)
