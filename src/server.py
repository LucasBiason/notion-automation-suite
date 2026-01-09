"""Entrypoint for the FastMCP-powered Notion server."""

from __future__ import annotations

from runtime import configure_logging, create_fastmcp_app, load_environment


def main() -> None:
    """Load configuration and start the FastMCP stdio server."""
    load_environment()
    configure_logging()
    app = create_fastmcp_app()
    app.run("stdio")


if __name__ == "__main__":
    main()
