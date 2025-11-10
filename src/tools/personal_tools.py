"""
Personal Notion MCP Tools

Provides specialized tools for personal database operations.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from custom.personal_notion import PersonalNotion
from utils.constants import PersonalStatus

logger = structlog.get_logger(__name__)

STATUS_OPTIONS = [status.value for status in PersonalStatus]
TEMPLATE_OPTIONS = sorted(PersonalNotion.TEMPLATES.keys())


class PersonalNotionTools:
    """Tools for personal database operations"""

    def __init__(self, personal_notion):
        self.personal_notion = personal_notion

    def _ensure_available(self) -> None:
        if self.personal_notion is None:
            raise ValueError(
                "Personal database is not configured for this MCP server. Configure NOTION_PERSONAL_DATABASE_ID first."
            )

    @staticmethod
    def _extract_data(payload: Dict[str, Any]) -> Optional[Dict[str, str]]:
        data = payload.pop("data", None)
        if data is None:
            return None

        start = data.get("start")
        if not start:
            raise ValueError("Field 'data.start' is required whenever 'data' is provided.")

        result = {"start": start}
        if "end" in data and data["end"]:
            result["end"] = data["end"]
        return result

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return tool metadata for the personal database."""
        return [
            {
                "name": "personal_create_task",
                "description": "Create a personal task or appointment using the 'Data' field.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": STATUS_OPTIONS,
                            "default": PersonalStatus.NAO_INICIADO.value,
                        },
                        "atividade": {"type": "string"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "start": {"type": "string", "description": "ISO 8601"},
                                "end": {"type": "string", "description": "ISO 8601"},
                            },
                        },
                        "descricao": {"type": "string"},
                        "icon": {"type": "string", "default": "👤"},
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "personal_create_subtask",
                "description": "Create a subtask linked to a parent task.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": STATUS_OPTIONS,
                            "default": PersonalStatus.NAO_INICIADO.value,
                        },
                        "data": {"type": "object"},
                        "descricao": {"type": "string"},
                        "icon": {"type": "string", "default": "✅"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "personal_use_template",
                "description": "Create a personal card using one of the generic templates.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "template_name": {
                            "type": "string",
                            "enum": TEMPLATE_OPTIONS,
                            "description": "Template identifier (e.g., weekly_planning).",
                        },
                        "reference_date": {
                            "type": "string",
                            "description": "Reference date for scheduling (YYYY-MM-DD).",
                        },
                        "overrides": {
                            "type": "object",
                            "description": "Optional overrides applied to the template payload.",
                        },
                    },
                    "required": ["template_name", "reference_date"],
                },
            },
            {
                "name": "personal_create_medical_appointment",
                "description": "Create medical appointments with duration and specialty.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "doctor": {"type": "string"},
                        "specialty": {"type": "string"},
                        "date": {"type": "string", "description": "ISO 8601"},
                        "duration_minutes": {"type": "integer", "default": 60},
                        "status": {
                            "type": "string",
                            "enum": STATUS_OPTIONS,
                            "default": PersonalStatus.NAO_INICIADO.value,
                        },
                    },
                    "required": ["doctor", "specialty", "date"],
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Dispatch personal tool calls."""
        logger.info("handling_personal_tool", tool=tool_name, args=arguments)
        self._ensure_available()

        if tool_name == "personal_create_task":
            data = self._extract_data(arguments)
            return await self.personal_notion.create_card(data=data, **arguments)

        if tool_name == "personal_create_subtask":
            data = self._extract_data(arguments)
            return await self.personal_notion.create_subitem(data=data, **arguments)

        if tool_name == "personal_use_template":
            reference = datetime.fromisoformat(arguments.pop("reference_date"))
            overrides = arguments.pop("overrides", None)
            template_name = arguments.get("template_name")
            return await self.personal_notion.use_template(
                template_name=template_name,
                reference_date=reference,
                overrides=overrides,
            )

        if tool_name == "personal_create_medical_appointment":
            appointment_date = datetime.fromisoformat(arguments.pop("date"))
            return await self.personal_notion.create_medical_appointment(
                date=appointment_date,
                **arguments,
            )

        raise ValueError(f"Unknown personal tool: {tool_name}")
