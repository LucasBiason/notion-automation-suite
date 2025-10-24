"""
Personal Notion MCP Tools

Provides specialized tools for personal database operations.
"""

from typing import Any, Dict, List

import structlog

logger = structlog.get_logger(__name__)


class PersonalNotionTools:
    """Tools for personal database operations"""

    def __init__(self, personal_notion):
        self.personal_notion = personal_notion

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get personal-specific tools"""
        return [
            {
                "name": "personal_create_task",
                "description": "Create personal task/event (uses 'Data' field, not 'Período')",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "atividade": {"type": "string"},
                        "data_start": {"type": "string", "description": "ISO datetime"},
                        "data_end": {"type": "string", "description": "ISO datetime"},
                        "status": {"type": "string", "default": "Para Fazer"},
                        "icon": {"type": "string", "description": "Emoji icon"},
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "personal_create_subtask",
                "description": "Create personal subtask linked to parent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "status": {"type": "string", "default": "Para Fazer"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "personal_create_event",
                "description": "Create personal event with specific template",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "atividade": {"type": "string"},
                        "data_start": {"type": "string", "description": "ISO datetime"},
                        "data_end": {"type": "string", "description": "ISO datetime"},
                        "template": {"type": "string", "description": "Event template type"},
                        "icon": {"type": "string", "description": "Emoji icon"},
                    },
                    "required": ["title", "atividade", "data_start"],
                },
            },
            {
                "name": "personal_create_recurring_event",
                "description": "Create recurring personal event",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "atividade": {"type": "string"},
                        "start_date": {"type": "string", "description": "ISO datetime"},
                        "end_date": {"type": "string", "description": "ISO datetime"},
                        "recurrence": {"type": "string", "description": "daily, weekly, monthly"},
                        "count": {"type": "number", "description": "Number of occurrences"},
                    },
                    "required": ["title", "atividade", "start_date", "recurrence"],
                },
            },
            {
                "name": "personal_update_status",
                "description": "Update personal task status",
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
                "name": "personal_reschedule",
                "description": "Reschedule personal task/event",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "new_start": {"type": "string", "description": "ISO datetime"},
                        "new_end": {"type": "string", "description": "ISO datetime"},
                    },
                    "required": ["page_id", "new_start"],
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Handle personal tool calls"""
        logger.info("handling_personal_tool", tool=tool_name, args=arguments)

        if tool_name == "personal_create_task":
            data = None
            if "data_start" in arguments:
                data = {"start": arguments.pop("data_start")}
                if "data_end" in arguments:
                    data["end"] = arguments.pop("data_end")
            return await self.personal_notion.create_card(data=data, **arguments)

        elif tool_name == "personal_create_subtask":
            return await self.personal_notion.create_subitem(**arguments)

        elif tool_name == "personal_create_event":
            data = {
                "start": arguments.pop("data_start"),
                "end": arguments.pop("data_end", arguments["data_start"]),
            }
            return await self.personal_notion.create_event(data=data, **arguments)

        elif tool_name == "personal_create_recurring_event":
            from datetime import datetime

            start = datetime.fromisoformat(arguments.pop("start_date"))
            end = None
            if "end_date" in arguments:
                end = datetime.fromisoformat(arguments.pop("end_date"))
            return await self.personal_notion.create_recurring_event(
                start_date=start, end_date=end, **arguments
            )

        elif tool_name == "personal_update_status":
            return await self.personal_notion.update_status(**arguments)

        elif tool_name == "personal_reschedule":
            from datetime import datetime

            new_start = datetime.fromisoformat(arguments.pop("new_start"))
            new_end = None
            if "new_end" in arguments:
                new_end = datetime.fromisoformat(arguments.pop("new_end"))
            return await self.personal_notion.reschedule(
                page_id=arguments["page_id"], new_start=new_start, new_end=new_end
            )

        else:
            raise ValueError(f"Unknown personal tool: {tool_name}")
