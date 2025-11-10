"""
Base MCP Tools for Notion Service

Provides low-level Notion API tools for MCP protocol.
"""

from typing import Any, Dict, List

import structlog

logger = structlog.get_logger(__name__)


class BaseNotionTools:
    """Base tools for Notion API operations"""

    def __init__(self, notion_service):
        self.service = notion_service

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get base Notion API tools"""
        return [
            {
                "name": "notion_create_page",
                "description": "Create a page in Notion database (low-level API)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "database_id": {"type": "string"},
                        "properties": {"type": "object"},
                        "icon": {"type": "object"},
                    },
                    "required": ["database_id", "properties"],
                },
            },
            {
                "name": "notion_update_page",
                "description": "Update a Notion page (low-level API)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "properties": {"type": "object"},
                        "icon": {"type": "object"},
                    },
                    "required": ["page_id"],
                },
            },
            {
                "name": "notion_get_page",
                "description": "Get a Notion page by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                    },
                    "required": ["page_id"],
                },
            },
            {
                "name": "notion_query_database",
                "description": "Query Notion database with filters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "database_id": {"type": "string"},
                        "filter": {"type": "object"},
                        "sorts": {"type": "array"},
                    },
                    "required": ["database_id"],
                },
            },
            {
                "name": "notion_delete_page",
                "description": "Delete/archive a Notion page",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "archived": {"type": "boolean", "default": True},
                    },
                    "required": ["page_id"],
                },
            },
            {
                "name": "notion_append_blocks",
                "description": "Append blocks to a Notion page",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "blocks": {"type": "array"},
                    },
                    "required": ["page_id", "blocks"],
                },
            },
            {
                "name": "notion_update_blocks",
                "description": "Update blocks in a Notion page",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "blocks": {"type": "array"},
                    },
                    "required": ["page_id", "blocks"],
                },
            },
            {
                "name": "notion_delete_blocks",
                "description": "Delete blocks from a Notion page",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "block_ids": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["page_id", "block_ids"],
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Handle base tool calls"""
        logger.info("handling_base_tool", tool=tool_name, args=arguments)

        if tool_name == "notion_create_page":
            return await self.service.create_page(**arguments)

        elif tool_name == "notion_update_page":
            return await self.service.update_page(**arguments)

        elif tool_name == "notion_get_page":
            return await self.service.get_page(**arguments)

        elif tool_name == "notion_query_database":
            return await self.service.query_database(**arguments)

        elif tool_name == "notion_delete_page":
            return await self.service.delete_page(**arguments)

        elif tool_name == "notion_append_blocks":
            return await self.service.append_blocks(**arguments)

        elif tool_name == "notion_update_blocks":
            return await self.service.update_blocks(**arguments)

        elif tool_name == "notion_delete_blocks":
            return await self.service.delete_blocks(**arguments)

        else:
            raise ValueError(f"Unknown base tool: {tool_name}")
