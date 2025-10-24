"""
Work Notion MCP Tools

Provides specialized tools for work database operations.
"""

from typing import Any, Dict, List

import structlog

logger = structlog.get_logger(__name__)


class WorkNotionTools:
    """Tools for work database operations"""

    def __init__(self, work_notion):
        self.work_notion = work_notion

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get work-specific tools"""
        return [
            {
                "name": "work_create_project",
                "description": "Create work project with correct structure (client, project, priority)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Project title (without emojis)",
                        },
                        "cliente": {"type": "string", "default": "Astracode"},
                        "projeto": {"type": "string", "description": "ExpenseIQ, HubTravel, etc"},
                        "prioridade": {"type": "string", "default": "Normal"},
                        "icon": {"type": "string", "description": "Emoji icon (e.g., 🚀)"},
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "work_create_task",
                "description": "Create work task linked to parent project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "prioridade": {"type": "string", "default": "Normal"},
                        "status": {"type": "string", "default": "Não iniciado"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "work_create_subitem",
                "description": "Create work subitem with correct hierarchy",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "prioridade": {"type": "string", "default": "Normal"},
                        "status": {"type": "string", "default": "Não iniciado"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "work_update_status",
                "description": "Update work item status",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "status": {"type": "string"},
                    },
                    "required": ["page_id", "status"],
                },
            },
            {
                "name": "work_update_priority",
                "description": "Update work item priority",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "prioridade": {"type": "string"},
                    },
                    "required": ["page_id", "prioridade"],
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Handle work tool calls"""
        logger.info("handling_work_tool", tool=tool_name, args=arguments)

        if tool_name == "work_create_project":
            return await self.work_notion.create_card(**arguments)

        elif tool_name == "work_create_task":
            return await self.work_notion.create_task(**arguments)

        elif tool_name == "work_create_subitem":
            return await self.work_notion.create_subitem(**arguments)

        elif tool_name == "work_update_status":
            return await self.work_notion.update_status(**arguments)

        elif tool_name == "work_update_priority":
            return await self.work_notion.update_priority(**arguments)

        else:
            raise ValueError(f"Unknown work tool: {tool_name}")
