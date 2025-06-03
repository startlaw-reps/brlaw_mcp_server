import logging

import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_logging() -> None:
    """Set the scraper tests up for running."""

    logging.getLogger("brlaw_mcp_server").setLevel(logging.DEBUG)
