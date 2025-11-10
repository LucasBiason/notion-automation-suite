"""Pacote raiz da Notion Automation Suite."""

from importlib.metadata import version, PackageNotFoundError

__all__ = ["get_version"]


def get_version() -> str:
    """Retorna a versão instalada do pacote."""
    try:
        return version("notion-automation-suite")
    except PackageNotFoundError:  # pragma: no cover
        return "0.0.0"
