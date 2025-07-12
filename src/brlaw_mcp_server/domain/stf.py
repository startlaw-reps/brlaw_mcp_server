import logging
import urllib.parse
from typing import TYPE_CHECKING, Self, cast, override

from brlaw_mcp_server.domain._base import BaseLegalPrecedent

if TYPE_CHECKING:
    from patchright.async_api import Page


_LOGGER = logging.getLogger(__name__)


class StfLegalPrecedent(BaseLegalPrecedent):
    """A legal precedent from the Supremo Tribunal Federal (STF)."""

    @override
    @classmethod
    async def research(
        cls, browser: "Page", *, summary_search_prompt: str, desired_page: int = 1
    ) -> "list[Self]":
        # Needed ahead to read the copied summaries.
        await browser.context.grant_permissions(["clipboard-read"])

        await browser.goto(
            " https://jurisprudencia.stf.jus.br/pages/search?"
            + urllib.parse.urlencode(
                {
                    "base": "acordaos",
                    "pesquisa_inteiro_teor": "false",
                    "sinonimo": "true",
                    "plural": "true",
                    "radicais": "false",
                    "buscaExata": "true",
                    "page": str(desired_page),
                    "pageSize": "10",
                    "queryString": summary_search_prompt,
                }
            ),
            # Page keeps loading async.
            wait_until="networkidle",
        )

        numbers_of_results_locators = await browser.locator(
            "div.mat-tooltip-trigger > span.ml-5.font-weight-500"
        ).all()

        if len(numbers_of_results_locators) == 0:
            raise RuntimeError("Failed to get the number of results")

        txt_numbers_of_precedents = await numbers_of_results_locators[0].text_content()
        if txt_numbers_of_precedents is None:
            raise RuntimeError("Failed to get the number of results")

        numbers_of_precedents = int(
            txt_numbers_of_precedents.strip("() ").replace(".", "")
        )

        if numbers_of_precedents == 0:
            return []

        results_locators = await browser.locator("div[id^=result-index-]").all()
        if len(results_locators) == 0:
            raise RuntimeError("Failed to find the results when there are results")

        return_value: list[Self] = []
        for result_locator in results_locators:
            await result_locator.locator("app-clipboard").click()
            handle = await browser.evaluate_handle(
                "() => navigator.clipboard.readText()"
            )
            summary = cast("str", await handle.json_value())

            return_value.append(
                cls(
                    summary=summary,
                )
            )

        return return_value
