"""Configuration helpers for the Notion MCP runtime."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, TextIO

import structlog
from dotenv import load_dotenv

from utils import DatabaseType

logger = structlog.get_logger(__name__)

DEFAULT_ENV_PATH = "config/.env"
ENV_PATH_VARIABLE = "NOTION_ENV_FILE"
LOG_FILE_VARIABLE = "LOG_FILE_PATH"
_DEFAULT_LOG_PATH = Path("logs/mcp.log")

_LOG_FILE_HANDLE: Optional[TextIO] = None


@dataclass(slots=True)
class NotionConfig:
    """Configuration container for MCP runtime components."""

    token: str
    database_ids: Dict[DatabaseType, str]


def load_config() -> NotionConfig:
    """Load Notion credentials and database ids from environment variables."""

    token = os.getenv("NOTION_API_TOKEN")
    if not token:
        raise ValueError("NOTION_API_TOKEN environment variable is required")

    database_ids = {
        DatabaseType.WORK: os.getenv("NOTION_WORK_DATABASE_ID", ""),
        DatabaseType.STUDIES: os.getenv("NOTION_STUDIES_DATABASE_ID", ""),
        DatabaseType.PERSONAL: os.getenv("NOTION_PERSONAL_DATABASE_ID", ""),
        DatabaseType.YOUTUBER: os.getenv("NOTION_YOUTUBER_DATABASE_ID", ""),
    }

    for db_type, db_id in database_ids.items():
        if not db_id:
            logger.warning(
                "database_id_missing",
                database_type=db_type.value,
                message=f"No database ID configured for {db_type.value}",
            )

    return NotionConfig(token=token, database_ids=database_ids)


def load_environment() -> None:
    """Load environment variables required by the MCP server.

    Priority order:
    1. Explicit path via ``NOTION_ENV_FILE`` environment variable.
    2. Project default ``config/.env``.
    3. Fallback to ``load_dotenv()`` search behaviour.
    """

    candidate = os.getenv(ENV_PATH_VARIABLE)
    if candidate:
        load_dotenv(candidate, override=True)
        return

    default_path = Path(DEFAULT_ENV_PATH)
    if default_path.exists():
        load_dotenv(default_path, override=True)
        return

    # Fallback to default .env discovery in current working directory hierarchy
    load_dotenv(override=True)


def configure_logging() -> None:
    """Configure structured logging for the MCP server."""

    global _LOG_FILE_HANDLE

    log_path = Path(os.getenv(LOG_FILE_VARIABLE, _DEFAULT_LOG_PATH))
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if _LOG_FILE_HANDLE is None or _LOG_FILE_HANDLE.closed:
        _LOG_FILE_HANDLE = log_path.open("a", encoding="utf-8")

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=_LOG_FILE_HANDLE),
    )
