"""Minimal entrypoint for the Notion MCP server."""

from __future__ import annotations

import asyncio

from runtime import (
    NotionMCPServer,
    configure_logging,
    load_environment,
    run_stdio_server,
)


def main() -> None:
    """Load configuration and start the stdio MCP server."""
    load_environment()
    configure_logging()

    async def _run() -> None:
        server = NotionMCPServer()
        await run_stdio_server(server)

    asyncio.run(_run())


if __name__ == "__main__":
    main()
