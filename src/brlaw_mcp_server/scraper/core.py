"""Core functionality for scraping legal data from official sources."""

from typing import TYPE_CHECKING, Final, Literal

from mcp.types import TextContent
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if TYPE_CHECKING:
    from typing import Literal

    from brlaw_mcp_server.scraper.webdriver import WebDriver

NO_RESULTS_MESSAGE: Final[str] = "Nenhum resultado encontrado"


async def scrape_legal_precedents(
    wd: "WebDriver", criteria: str, court: "Literal['STJ']"
) -> list[TextContent]:
    """Scrape legal precedents from official sources.

    :param wd: The webdriver to use.
    :param criteria: The criteria to search for.
    :param court: The court that authored the precedent.
    :return: A list of TextContent objects explaining what was found."""

    if court != "STJ":
        raise NotImplementedError("Only STJ is supported at the moment")  # pyright: ignore[reportUnreachable]

    wd.get("https://scon.stj.jus.br/SCON/")

    wd.find_element(value="idMostrarPesquisaAvancada").click()

    ementa = wd.find_element(value="ementa")
    ementa.send_keys(criteria)
    ementa.send_keys(Keys.ENTER)

    wd.wait_for_element_to_be_visible("#corpopaginajurisprudencia")

    data = wd.find_elements(by=By.CSS_SELECTOR, value="[id^=textSemformatacao]")

    if len(data) == 0:
        try:
            el_error_message = wd.find_element(
                by=By.CSS_SELECTOR, value="div.erroMensagem"
            )
        except NoSuchElementException as e:
            raise RuntimeError("Unexpected behavior from requested service") from e

        if (
            el_error_message.get_attribute("textContent")  # pyright: ignore[reportUnknownMemberType]
            == "Nenhum documento encontrado!"
        ):
            return [TextContent(type="text", text=NO_RESULTS_MESSAGE)]

    return [
        TextContent(type="text", text=text)
        for el in data
        if (text := el.get_attribute("textContent")) is not None  # pyright: ignore[reportUnknownMemberType]
    ]
