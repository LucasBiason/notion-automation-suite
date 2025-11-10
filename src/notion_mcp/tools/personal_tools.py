"""
Personal Notion MCP Tools

Provides specialized tools for personal database operations.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from notion_mcp.custom.personal_notion import PersonalNotion
from notion_mcp.utils.constants import PersonalStatus

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
            raise ValueError("Campo 'data.start' é obrigatório quando 'data' é informado.")

        result = {"start": start}
        if "end" in data and data["end"]:
            result["end"] = data["end"]
        return result

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return tool metadata for the personal database."""
        return [
            {
                "name": "personal_create_task",
                "description": "Criar tarefa ou compromisso pessoal usando o campo 'Data'.",
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
                "description": "Criar subtarefa vinculada a uma tarefa principal.",
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
                "description": "Criar card pessoal utilizando um template pré-definido.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "template_name": {"type": "string", "enum": TEMPLATE_OPTIONS},
                        "reference_date": {
                            "type": "string",
                            "description": "Data base para o template (YYYY-MM-DD).",
                        },
                        "overrides": {
                            "type": "object",
                            "description": "Sobrescrições opcionais dos campos do template.",
                        },
                    },
                    "required": ["template_name", "reference_date"],
                },
            },
            {
                "name": "personal_create_weekly_cards",
                "description": "Gerar cards semanais padrão (Planejamento, Hamilton, Tratamento).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "week_start": {
                            "type": "string",
                            "description": "Data da segunda-feira da semana (YYYY-MM-DD).",
                        },
                        "overrides": {
                            "type": "object",
                            "additionalProperties": {"type": "object"},
                            "description": "Sobrescrições por template (ex: {hamilton: ...}).",
                        },
                    },
                    "required": ["week_start"],
                },
            },
            {
                "name": "personal_create_monthly_events",
                "description": "Gerar eventos mensais padrão (NF, Fechamento, Revisão).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "integer"},
                        "month": {"type": "integer", "minimum": 1, "maximum": 12},
                        "overrides": {
                            "type": "object",
                            "additionalProperties": {"type": "object"},
                        },
                    },
                    "required": ["year", "month"],
                },
            },
            {
                "name": "personal_create_medical_appointment",
                "description": "Criar consulta médica com duração e especialidade.",
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
            return await self.personal_notion.use_template(
                template_name=arguments["template_name"],
                reference_date=reference,
                overrides=overrides,
            )

        if tool_name == "personal_create_weekly_cards":
            week_start = datetime.fromisoformat(arguments.pop("week_start"))
            overrides = arguments.pop("overrides", None)
            return await self.personal_notion.create_weekly_cards(
                week_start=week_start,
                overrides=overrides,
            )

        if tool_name == "personal_create_monthly_events":
            overrides = arguments.pop("overrides", None)
            return await self.personal_notion.create_monthly_events(
                overrides=overrides,
                **arguments,
            )

        if tool_name == "personal_create_medical_appointment":
            appointment_date = datetime.fromisoformat(arguments.pop("date"))
            return await self.personal_notion.create_medical_appointment(
                date=appointment_date,
                **arguments,
            )

        raise ValueError(f"Unknown personal tool: {tool_name}")
