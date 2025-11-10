"""Core runtime server that wires Notion-specific tooling."""

from __future__ import annotations

import os
import json
from typing import Any, Awaitable, Callable, Dict, List, Optional

import structlog

from custom import PersonalNotion, StudyNotion, WorkNotion, YoutuberNotion
from services.notion_service import NotionService
from tools import (
    BaseNotionTools,
    PersonalNotionTools,
    StudyNotionTools,
    WorkNotionTools,
    YoutuberNotionTools,
)
from utils import DatabaseType
from .config import NotionConfig

logger = structlog.get_logger(__name__)


class NotionMCPServer:
    """Wires Notion business rules into MCP tool definitions."""

    def __init__(self) -> None:
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is required")

        self.database_ids = {
            DatabaseType.WORK: os.getenv("NOTION_WORK_DATABASE_ID"),
            DatabaseType.STUDIES: os.getenv("NOTION_STUDIES_DATABASE_ID"),
            DatabaseType.PERSONAL: os.getenv("NOTION_PERSONAL_DATABASE_ID"),
            DatabaseType.YOUTUBER: os.getenv("NOTION_YOUTUBER_DATABASE_ID"),
        }

        for db_type, db_id in self.database_ids.items():
            if not db_id:
                logger.warning(
                    "database_id_missing",
                    database_type=db_type.value,
                    message=f"No database ID configured for {db_type.value}",
                )

        self.service = NotionService(self.token)

        self.work_notion = (
            WorkNotion(self.service, self.database_ids[DatabaseType.WORK])
            if self.database_ids[DatabaseType.WORK]
            else None
        )
        self.study_notion = (
            StudyNotion(self.service, self.database_ids[DatabaseType.STUDIES])
            if self.database_ids[DatabaseType.STUDIES]
            else None
        )
        self.youtuber_notion = (
            YoutuberNotion(self.service, self.database_ids[DatabaseType.YOUTUBER])
            if self.database_ids[DatabaseType.YOUTUBER]
            else None
        )
        self.personal_notion = (
            PersonalNotion(self.service, self.database_ids[DatabaseType.PERSONAL])
            if self.database_ids[DatabaseType.PERSONAL]
            else None
        )

        self._tool_definitions: List[Dict[str, Any]] = []
        self._tool_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[Any]]] = {}

        self.base_tools = BaseNotionTools(self.service)
        self.work_tools = WorkNotionTools(self.work_notion) if self.work_notion else None
        self.study_tools = StudyNotionTools(self.study_notion) if self.study_notion else None
        self.youtuber_tools = (
            YoutuberNotionTools(self.youtuber_notion) if self.youtuber_notion else None
        )
        self.personal_tools = (
            PersonalNotionTools(self.personal_notion) if self.personal_notion else None
        )

        self._initialize_tool_registry()

        logger.info(
            "mcp_server_initialized",
            work_enabled=self.work_notion is not None,
            study_enabled=self.study_notion is not None,
            youtuber_enabled=self.youtuber_notion is not None,
            personal_enabled=self.personal_notion is not None,
        )

    async def close(self) -> None:
        await self.service.close()
        logger.info("mcp_server_closed")

    def get_tools(self) -> List[Dict[str, Any]]:
        return list(self._tool_definitions)

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        logger.info("handling_tool_call", tool=tool_name, args=arguments)
        handler = self._tool_handlers.get(tool_name)
        if handler is None:
            raise ValueError(f"Unknown tool: {tool_name}")
        return await handler(arguments)

    def get_resources(self) -> List[Dict[str, Any]]:
        resources: List[Dict[str, Any]] = []
        for db_type, db_id in self.database_ids.items():
            if not db_id:
                continue
            resources.append(
                {
                    "uri": f"notion://database/{db_type.value}",
                    "name": f"{db_type.value.title()} Database",
                    "description": (
                        "Esquema completo da base do Notion utilizada pelo MCP "
                        f"({db_type.value})."
                    ),
                    "mimeType": "application/json",
                }
            )
        return resources

    async def read_resource(self, uri: str) -> Dict[str, Any]:
        if not uri:
            raise ValueError("Resource URI is required")

        prefix = "notion://database/"
        if not uri.startswith(prefix):
            raise ValueError(f"Unsupported resource URI: {uri}")

        db_key = uri[len(prefix) :]
        try:
            database_type = DatabaseType(db_key)
        except ValueError as exc:  # pragma: no cover - defensive logging
            raise ValueError(f"Unknown database resource: {uri}") from exc

        database_id = self.database_ids.get(database_type)
        if not database_id:
            raise ValueError(f"Database ID for {database_type.value} is not configured")

        schema = await self.service.get_database(database_id)
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(schema, ensure_ascii=False),
        }

    def get_prompts(self) -> List[Dict[str, Any]]:
        return []

    def _initialize_tool_registry(self) -> None:
        self._register_tool_set(self.base_tools, self.base_tools.handle_tool_call)
        self._register_tool_set(
            self.work_tools,
            self.work_tools.handle_tool_call if self.work_tools else None,
        )
        self._register_tool_set(
            self.study_tools,
            self.study_tools.handle_tool_call if self.study_tools else None,
        )
        self._register_tool_set(
            self.youtuber_tools,
            self.youtuber_tools.handle_tool_call if self.youtuber_tools else None,
        )
        self._register_tool_set(
            self.personal_tools,
            self.personal_tools.handle_tool_call if self.personal_tools else None,
        )

    def _register_tool_set(
        self,
        tool_provider: Optional[Any],
        handler: Optional[Callable[[str, Dict[str, Any]], Awaitable[Any]]],
    ) -> None:
        if tool_provider is None or handler is None:
            return
        for definition in tool_provider.get_tools():
            name = definition.get("name")
            if not name:
                raise ValueError("Tool definition missing 'name'")
            if name in self._tool_handlers:
                raise ValueError(f"Duplicated tool registration: {name}")
            self._tool_definitions.append(definition)
            self._tool_handlers[name] = self._make_tool_invoker(handler, name)

    @staticmethod
    def _make_tool_invoker(
        handler: Callable[[str, Dict[str, Any]], Awaitable[Any]],
        tool_name: str,
    ) -> Callable[[Dict[str, Any]], Awaitable[Any]]:
        async def _invoke(arguments: Dict[str, Any]) -> Any:
            return await handler(tool_name, arguments)

        return _invoke

