from typing import TYPE_CHECKING, Self, override

from brlaw_mcp_server.domain.stj import StjLegalPrecedent

if TYPE_CHECKING:
    from patchright.async_api import Page


class TjspLegalPrecedent(StjLegalPrecedent):
    """Model for a legal precedent from the Tribunal de Justiça de São Paulo (TJSP)."""

    @override
    @classmethod
    async def research(cls, page: "Page", *, summary: str) -> "list[Self]":
        """Scrape legal precedents from the Tribunal de Justiça de São Paulo (TJSP)."""

        await page.goto("https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do")

        for _ in range(3):
            try:
                ementa_input_field = wd.find_element(value="iddados.buscaEmenta")
            except NoSuchElementException as e:
                raise RuntimeError(
                    "The scraper wasn't able to find the 'ementa' input field"
                ) from e

            ementa_input_field.clear()
            ementa_input_field.send_keys(criteria)

            _LOGGER.debug("Requesting results")
            ementa_input_field.send_keys(Keys.ENTER)

            _LOGGER.debug("Waiting for the expected response")
            try:
                wd.wait_for_element_to_be_visible("#tabs", timeout=5)
            except TimeoutException as e:
                return_messages = wd.find_elements(
                    by=By.CSS_SELECTOR, value="#mensagemRetorno > li"
                )

                if (
                    len(return_messages) == 0
                    or (text := return_messages[0].get_attribute("textContent")) is None  # pyright: ignore[reportUnknownMemberType]
                ):
                    raise RuntimeError(
                        "Could not find the expected response under the timeout limit and no "
                        + "explanatory messages were found"
                    ) from e

                if "reCAPTCHA" in text:
                    _LOGGER.debug("reCAPTCHA validation failed")
                    await asyncio.sleep(2)
                    continue
            else:
                break
        else:
            raise RuntimeError(
                "Could not find the results table under the timeout limit after 3 attempts"
            )

        if (
            int(
                wd.find_element(value="totalResultadoAba-A").get_attribute("value")  # pyright: ignore[reportUnknownMemberType, reportArgumentType]
            )
            == 0
        ):
            return []

        els_ementa = wd.find_elements(
            by=By.CSS_SELECTOR,
            value=">".join(
                [
                    "#divDadosResultado-A",
                    "table",
                    "tbody",
                    "tr.fundocinza1",
                    "td:nth-child(2)",
                    "table",
                    "tbody",
                    "tr:nth-child(8)",
                ]
            ),
        )

        result = [
            cls(
                text=el.get_attribute("textContent").strip(),  # pyright: ignore[reportUnknownMemberType, reportOptionalMemberAccess]
            )
            for el in els_ementa
        ]

        if len(result) == 0:
            raise RuntimeError("No results were found, but more than one was expected")

        return result
