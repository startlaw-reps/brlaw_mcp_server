"""Tests for the core server functionality."""

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "arguments"),
    [
        pytest.param(
            "invalid_tool",
            {},
            marks=pytest.mark.xfail(
                strict=True, reason="Invalid tool name", raises=AssertionError
            ),
            id="invalid_tool_name",
        ),
        pytest.param(
            "pesquisar_precedentes_judiciais",
            {"criteria": "test criteria"},
            marks=pytest.mark.xfail(
                strict=True, reason="Missing court argument", raises=AssertionError
            ),
            id="missing_court_argument",
        ),
        pytest.param(
            "pesquisar_precedentes_judiciais",
            {"criteria": "test criteria", "court": "STJ"},
            id="valid_tool_call",
        ),
    ],
)
async def test_call_tool(
    tool_name: str,
    arguments: dict[str, str],
) -> None:
    """Test calling a server's tool."""
    from pathlib import Path

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp.types import TextContent

    async with (
        stdio_client(
            StdioServerParameters(
                command="uv",
                args=[
                    "--directory",
                    str(Path(__file__).parent.parent.absolute()),
                    "run",
                    "brlaw_mcp_server",
                ],
            )
        ) as (read, write),
        ClientSession(
            read_stream=read,
            write_stream=write,
        ) as client,
    ):
        await client.initialize()
        assert len((await client.list_tools()).tools) > 0

        results = await client.call_tool(tool_name, arguments)

    assert not results.isError
    assert isinstance(results.content, list)
    assert all(isinstance(content, TextContent) for content in results.content)
