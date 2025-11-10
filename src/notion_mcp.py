"""
Notion MCP Server compatibility module.

Exposes public API and behaves like the original ``notion_mcp`` package
while the source tree lives directly under ``src/``.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

__version__ = "0.1.0"
__author__ = "Lucas Biason"
__email__ = "lucas.biason@gmail.com"

# Allow ``import notion_mcp.<submodule>`` to resolve modules located in ``src/``
__path__ = [str(Path(__file__).parent)]
if __spec__ is not None:  # pragma: no coverage - defensive guard
    __spec__.submodule_search_locations = __path__

from custom.personal_notion import PersonalNotion
from custom.study_notion import StudyNotion
from custom.work_notion import WorkNotion
from custom.youtuber_notion import YoutuberNotion
from services.notion_service import NotionService

__all__ = [
    "NotionService",
    "WorkNotion",
    "StudyNotion",
    "YoutuberNotion",
    "PersonalNotion",
]

_SUBMODULES = ("custom", "exceptions", "runtime", "services", "tools", "utils")
for _name in _SUBMODULES:
    _module = importlib.import_module(_name)
    sys.modules[f"{__name__}.{_name}"] = _module
