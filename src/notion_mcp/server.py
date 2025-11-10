"""
MCP Server for Notion Integration

Implements Model Context Protocol server with custom Notion tools.
"""

import asyncio
import json
import os
import sys
from typing import Any, Awaitable, Callable, Dict, List, Optional

import structlog
from dotenv import load_dotenv

from notion_mcp.custom import PersonalNotion, StudyNotion, WorkNotion, YoutuberNotion
from notion_mcp.services.notion_service import NotionService
from notion_mcp.tools import (
    BaseNotionTools,
    PersonalNotionTools,
    StudyNotionTools,
    WorkNotionTools,
    YoutuberNotionTools,
)
from notion_mcp.utils import DatabaseType

# Load environment variables
load_dotenv()

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger(__name__)


class NotionMCPServer:
    """
    MCP Server for Notion Integration

    Provides tools for AI agents to interact with Notion using
    custom business rules for different database types.
    """

    def __init__(self):
        """Initialize MCP server"""
        # Load configuration
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is required")

        self.database_ids = {
            DatabaseType.WORK: os.getenv("NOTION_WORK_DATABASE_ID"),
            DatabaseType.STUDIES: os.getenv("NOTION_STUDIES_DATABASE_ID"),
            DatabaseType.PERSONAL: os.getenv("NOTION_PERSONAL_DATABASE_ID"),
            DatabaseType.YOUTUBER: os.getenv("NOTION_YOUTUBER_DATABASE_ID"),
        }

        # Validate database IDs
        for db_type, db_id in self.database_ids.items():
            if not db_id:
                logger.warning(
                    "database_id_missing",
                    database_type=db_type.value,
                    message=f"No database ID configured for {db_type.value}",
                )

        # Initialize service
        self.service = NotionService(self.token)

        # Initialize custom implementations
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

        # Initialize tool handlers
        self.base_tools = BaseNotionTools(self.service)
        self.work_tools = WorkNotionTools(self.work_notion) if self.work_notion else None
        self.study_tools = StudyNotionTools(self.study_notion) if self.study_notion else None
        self.youtuber_tools = (
            YoutuberNotionTools(self.youtuber_notion) if self.youtuber_notion else None
        )
        self.personal_tools = (
            PersonalNotionTools(self.personal_notion) if self.personal_notion else None
        )

        self._tool_definitions: List[Dict[str, Any]] = []
        self._tool_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[Any]]] = {}
        self._initialize_tool_registry()

        logger.info(
            "mcp_server_initialized",
            work_enabled=self.work_notion is not None,
            study_enabled=self.study_notion is not None,
            youtuber_enabled=self.youtuber_notion is not None,
            personal_enabled=self.personal_notion is not None,
        )

    async def close(self) -> None:
        """Close server and cleanup resources"""
        await self.service.close()
        logger.info("mcp_server_closed")

    def get_tools(self) -> list:
        """
        Get all available MCP tools

        Returns:
            List of tool definitions for MCP protocol
        """
        return list(self._tool_definitions)

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle MCP tool call

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        logger.info("handling_tool_call", tool=tool_name, args=arguments)
        handler = self._tool_handlers.get(tool_name)
        if handler is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        return await handler(arguments)

    def _initialize_tool_registry(self) -> None:
        """Register all available tool definitions with their handlers."""
        self._register_tool_set(self.base_tools, self.base_tools.handle_tool_call)
        self._register_tool_set(self.work_tools, self.work_tools.handle_tool_call if self.work_tools else None)
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

    def get_resources(self) -> List[Dict[str, Any]]:
        """Return resource descriptors for configured databases."""
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
        """Read resource content referenced by URI."""
        if not uri:
            raise ValueError("Resource URI is required")

        prefix = "notion://database/"
        if not uri.startswith(prefix):
            raise ValueError(f"Unsupported resource URI: {uri}")

        db_key = uri[len(prefix) :]
        try:
            database_type = DatabaseType(db_key)
        except ValueError as exc:  # noqa: F841 - we log a clear error below
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
        """Return registered conversational prompts (none for now)."""
        return []


class MCPStdIOServer:
    """Minimal MCP stdio server implementation for Cursor integration."""

    def __init__(self, notion_server: NotionMCPServer):
        self._notion_server = notion_server

    async def run(self) -> None:
        """Run stdio loop handling MCP JSON-RPC requests."""
        loop = asyncio.get_running_loop()
        logger.info("mcp_stdio_server_started")

        try:
            while True:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if line == "":
                    break

                stripped = line.strip()
                if not stripped:
                    continue

                response = await self._handle_line(stripped)
                if response is not None:
                    await self._write_response(response)

        except KeyboardInterrupt:
            logger.info("mcp_stdio_interrupted")
        finally:
            await self._notion_server.close()
            logger.info("mcp_stdio_server_stopped")

    async def _handle_line(self, raw_line: str) -> Optional[Dict[str, Any]]:
        try:
            request = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            logger.error("invalid_json", error=str(exc))
            return self._build_error_response(None, -32700, f"Invalid JSON: {exc.msg}")

        try:
            return await self._handle_request(request)
        except Exception as exc:  # noqa: BLE001 - intentional broad catch to reply via MCP
            logger.error("request_processing_error", error=str(exc))
            return self._build_error_response(
                request.get("id"),
                -32603,
                str(exc),
            )

    async def _handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        request_id = request.get("id")

        if method == "initialize":
            result = {
                "capabilities": {
                    "tools": {"list": True, "call": True},
                    "resources": {"list": True, "read": True},
                    "prompts": {"list": True},
                }
            }
            return self._build_success_response(request_id, result)

        if method == "tools/list":
            tools = self._notion_server.get_tools()
            return self._build_success_response(request_id, {"tools": tools})

        if method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {}) if params else {}

            if not tool_name:
                raise ValueError("Tool name is required for tools/call")

            result = await self._notion_server.handle_tool_call(tool_name, arguments)
            content = [
                {
                    "type": "text",
                    "text": json.dumps(result, ensure_ascii=False),
                }
            ]
            return self._build_success_response(request_id, {"content": content})

        if method == "resources/list":
            resources = self._notion_server.get_resources()
            return self._build_success_response(request_id, {"resources": resources})

        if method == "resources/read":
            params = request.get("params", {})
            uri = params.get("uri") if params else None
            resource_content = await self._notion_server.read_resource(uri)
            return self._build_success_response(request_id, {"contents": [resource_content]})

        if method == "prompts/list":
            prompts = self._notion_server.get_prompts()
            return self._build_success_response(request_id, {"prompts": prompts})

        if method == "notifications/subscribe":
            # No-op subscription support
            return self._build_success_response(request_id, {})

        if method == "ping":
            return self._build_success_response(request_id, {"pong": True})

        raise ValueError(f"Unknown method: {method}")

    @staticmethod
    def _build_success_response(request_id: Any, result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        response: Dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
        response["result"] = result or {}
        return response

    @staticmethod
    def _build_error_response(request_id: Any, code: int, message: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message,
            },
        }

    async def _write_response(self, response: Dict[str, Any]) -> None:
        """Write response JSON to stdout without blocking event loop."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._print_response, response)

    @staticmethod
    def _print_response(response: Dict[str, Any]) -> None:
        print(json.dumps(response), flush=True)


async def _async_main() -> None:
    logger.info("starting_mcp_server")
    server = NotionMCPServer()
    stdio_server = MCPStdIOServer(server)
    await stdio_server.run()
    logger.info("mcp_server_shutdown")


def main() -> None:
    """Entry point for MCP stdio execution."""
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
