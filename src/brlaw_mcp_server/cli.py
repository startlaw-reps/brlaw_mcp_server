"""CLI entrypoint."""

import click


@click.command()
@click.option("-v", "--verbose", count=True)
def main(verbose: bool) -> None:
    """MCP Server - Jurisprudência functionality for MCP"""
    import asyncio
    import logging
    import sys

    import brlaw_mcp_server.server.core as server

    logging_level = logging.WARNING
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:  # noqa: PLR2004
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()
