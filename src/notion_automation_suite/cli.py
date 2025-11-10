"""CLI consolidada para operações locais da Notion Automation Suite."""

from __future__ import annotations

import typer
from rich import print

app = typer.Typer(help="Ferramentas utilitárias para operar a suite de automações do Notion.")


@app.command()
def info() -> None:
    """Exibe informações básicas sobre a instalação."""
    print("[bold green]Notion Automation Suite[/bold green]")
    print("- CLI consolidada viva.")


if __name__ == "__main__":  # pragma: no cover
    app()
