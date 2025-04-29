"""Tests for the core server functionality."""

import pytest
from mcp.types import TextContent


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "arguments"),
    [
        pytest.param(
            "invalid_tool",
            ...,
            marks=pytest.mark.xfail(
                strict=True, reason="Invalid tool name", raises=ValueError
            ),
        ),
        pytest.param(
            "pesquisar_precedentes_judiciais",
            {"criteria": "test criteria"},
            marks=pytest.mark.xfail(
                strict=True, reason="Missing court argument", raises=KeyError
            ),
        ),
        (
            "pesquisar_precedentes_judiciais",
            {"criteria": "test criteria", "court": "STJ"},
        ),
    ],
)
async def test_call_tool(
    tool_name: str,
    arguments: dict[str, str],
) -> None:
    """Test calling a server's tool."""
    from brlaw_mcp_server.server.core import call_tool

    results = await call_tool(tool_name, arguments)

    assert isinstance(results, list)
    assert all(isinstance(result, TextContent) for result in results)
