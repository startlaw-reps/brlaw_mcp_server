from typing import TYPE_CHECKING, Final

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

import brlaw_mcp_server.scraper.core as scraper
from brlaw_mcp_server.scraper.webdriver import WebDriver
from brlaw_mcp_server.server import input_schemas

if TYPE_CHECKING:
    from typing import Any

_TOOLS: Final[list[Tool]] = [
    Tool(
        name="pesquisar_precedentes_judiciais",
        description="Pesquisa os precedentes judiciais que satisfaçam os critérios passados",
        inputSchema=input_schemas.RequisitarPrecedentesJudiciais.model_json_schema(),
    )
]


async def _list_tools() -> list["Tool"]:
    return _TOOLS


async def call_tool(
    name: str,
    arguments: dict[str, "Any"],  # pyright: ignore[reportExplicitAny]
) -> list[TextContent]:
    """Handles a tool call from a MCP client."""
    if name == "pesquisar_precedentes_judiciais":
        with WebDriver() as wd:
            return await scraper.scrape_legal_precedents(
                wd,
                arguments["criteria"],  # pyright: ignore[reportAny]
                arguments["court"],  # pyright: ignore[reportAny]
            )
    raise ValueError(f"Tool {name} not found")


async def serve() -> None:
    server = Server("brlaw_mcp_server")

    server.list_tools()(_list_tools)
    server.call_tool()(call_tool)

    options = server.create_initialization_options()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
