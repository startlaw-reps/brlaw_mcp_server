from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from patchright.async_api import async_playwright

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from patchright.async_api import Browser


@asynccontextmanager
async def browser_factory(headless: bool = True) -> "AsyncGenerator[Browser, None]":
    async with (
        async_playwright() as playwright,
        await playwright.chromium.launch(headless=headless) as browser,
    ):
        yield browser
