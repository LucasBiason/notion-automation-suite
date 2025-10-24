"""
Study Notion MCP Tools

Provides specialized tools for study database operations.
"""

from typing import Any, Dict, List

import structlog

logger = structlog.get_logger(__name__)


class StudyNotionTools:
    """Tools for study database operations"""

    def __init__(self, study_notion):
        self.study_notion = study_notion

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get study-specific tools"""
        return [
            {
                "name": "study_create_course",
                "description": "Create study course (without time, only dates)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "categorias": {"type": "array", "items": {"type": "string"}},
                        "periodo_start": {"type": "string", "description": "YYYY-MM-DD"},
                        "periodo_end": {"type": "string", "description": "YYYY-MM-DD"},
                        "icon": {"type": "string", "description": "Emoji icon"},
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "study_create_phase",
                "description": "Create course phase (subitem of course)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "periodo_start": {"type": "string", "description": "YYYY-MM-DD"},
                        "periodo_end": {"type": "string", "description": "YYYY-MM-DD"},
                        "icon": {"type": "string", "description": "Emoji icon"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "study_create_section",
                "description": "Create course section (subitem of phase)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "periodo_start": {"type": "string", "description": "YYYY-MM-DD"},
                        "periodo_end": {"type": "string", "description": "YYYY-MM-DD"},
                        "icon": {"type": "string", "description": "Emoji icon"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "study_create_class",
                "description": "Create study class with correct hours (19:00-21:00, Tuesday 19:30)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "start_time": {"type": "string", "description": "ISO datetime"},
                        "duration_minutes": {"type": "number"},
                        "status": {"type": "string", "default": "Para Fazer"},
                    },
                    "required": ["parent_id", "title", "start_time", "duration_minutes"],
                },
            },
            {
                "name": "study_reschedule",
                "description": "Reschedule study items (respects study hours)",
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
            {
                "name": "study_mark_completed",
                "description": "Mark study item as completed",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                    },
                    "required": ["page_id"],
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Handle study tool calls"""
        logger.info("handling_study_tool", tool=tool_name, args=arguments)

        if tool_name == "study_create_course":
            periodo = None
            if "periodo_start" in arguments:
                periodo = {"start": arguments.pop("periodo_start")}
                if "periodo_end" in arguments:
                    periodo["end"] = arguments.pop("periodo_end")
            return await self.study_notion.create_card(periodo=periodo, **arguments)

        elif tool_name == "study_create_phase":
            periodo = None
            if "periodo_start" in arguments:
                periodo = {"start": arguments.pop("periodo_start")}
                if "periodo_end" in arguments:
                    periodo["end"] = arguments.pop("periodo_end")
            return await self.study_notion.create_phase(periodo=periodo, **arguments)

        elif tool_name == "study_create_section":
            periodo = None
            if "periodo_start" in arguments:
                periodo = {"start": arguments.pop("periodo_start")}
                if "periodo_end" in arguments:
                    periodo["end"] = arguments.pop("periodo_end")
            return await self.study_notion.create_section(periodo=periodo, **arguments)

        elif tool_name == "study_create_class":
            from datetime import datetime

            start = datetime.fromisoformat(arguments.pop("start_time"))
            return await self.study_notion.create_class(start_time=start, **arguments)

        elif tool_name == "study_reschedule":
            from datetime import datetime

            new_start = datetime.fromisoformat(arguments.pop("new_start"))
            new_end = None
            if "new_end" in arguments:
                new_end = datetime.fromisoformat(arguments.pop("new_end"))
            return await self.study_notion.reschedule(
                page_id=arguments["page_id"], new_start=new_start, new_end=new_end
            )

        elif tool_name == "study_mark_completed":
            return await self.study_notion.mark_completed(arguments["page_id"])

        else:
            raise ValueError(f"Unknown study tool: {tool_name}")
