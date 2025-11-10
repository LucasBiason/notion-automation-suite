"""
Study Notion MCP Tools

Provides specialized tools for study database operations.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from notion_mcp.utils.constants import StudiesStatus

logger = structlog.get_logger(__name__)

STATUS_OPTIONS = [status.value for status in StudiesStatus]


class StudyNotionTools:
    """Tools for study database operations"""

    def __init__(self, study_notion):
        self.study_notion = study_notion

    def _ensure_available(self) -> None:
        if self.study_notion is None:
            raise ValueError(
                "Study database is not configured for this MCP server. Configure NOTION_STUDIES_DATABASE_ID first."
            )

    @staticmethod
    def _extract_period(payload: Dict[str, Any]) -> Optional[Dict[str, str]]:
        periodo = payload.pop("periodo", None)
        if periodo is None:
            return None

        start = periodo.get("start")
        if not start:
            raise ValueError("Campo 'periodo.start' é obrigatório quando 'periodo' é informado.")

        end = periodo.get("end")
        result = {"start": start}
        if end:
            result["end"] = end
        return result

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return tool metadata for the studies database."""
        return [
            {
                "name": "study_create_course",
                "description": "Criar curso ou trilha de estudos (sem horário, apenas datas).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "status": {"type": "string", "enum": STATUS_OPTIONS, "default": StudiesStatus.PARA_FAZER.value},
                        "categorias": {"type": "array", "items": {"type": "string"}},
                        "periodo": {
                            "type": "object",
                            "properties": {
                                "start": {"type": "string", "description": "YYYY-MM-DD"},
                                "end": {"type": "string", "description": "YYYY-MM-DD"},
                            },
                        },
                        "tempo_total": {"type": "string", "description": "Carga horária total"},
                        "descricao": {"type": "string"},
                        "icon": {"type": "string"},
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "study_create_course_complete",
                "description": "Criar curso completo com fases, seções e aulas.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "sinopse": {"type": "string"},
                        "categorias": {"type": "array", "items": {"type": "string"}},
                        "periodo": {
                            "type": "object",
                            "properties": {
                                "start": {"type": "string", "description": "YYYY-MM-DD"},
                                "end": {"type": "string", "description": "YYYY-MM-DD"},
                            },
                        },
                        "icon": {"type": "string"},
                        "fases": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "periodo": {"type": "object"},
                                    "descricao": {"type": "string"},
                                    "icon": {"type": "string"},
                                    "sections": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "title": {"type": "string"},
                                                "periodo": {"type": "object"},
                                                "descricao": {"type": "string"},
                                                "icon": {"type": "string"},
                                                "classes": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "title": {"type": "string"},
                                                            "start": {"type": "string", "description": "ISO 8601"},
                                                            "duration_minutes": {"type": "integer"},
                                                            "status": {"type": "string", "enum": STATUS_OPTIONS},
                                                            "icon": {"type": "string"},
                                                            "descricao": {"type": "string"},
                                                        },
                                                        "required": ["title", "start", "duration_minutes"],
                                                    },
                                                },
                                            },
                                            "required": ["title"],
                                        },
                                    },
                                },
                                "required": ["title"],
                            },
                        },
                    },
                    "required": ["title", "sinopse"],
                },
            },
            {
                "name": "study_create_phase",
                "description": "Criar fase de estudo vinculada a um curso.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "periodo": {"type": "object"},
                        "tempo_total": {"type": "string"},
                        "descricao": {"type": "string"},
                        "icon": {"type": "string", "default": "📖"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "study_create_section",
                "description": "Criar seção vinculada a uma fase ou curso.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "periodo": {"type": "object"},
                        "tempo_total": {"type": "string"},
                        "descricao": {"type": "string"},
                        "icon": {"type": "string", "default": "📑"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "study_create_class",
                "description": "Criar aula com horário padronizado (19h-21h, terça 19h30).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "start_time": {"type": "string", "description": "ISO 8601"},
                        "duration_minutes": {"type": "integer", "minimum": 1},
                        "status": {"type": "string", "enum": STATUS_OPTIONS, "default": StudiesStatus.PARA_FAZER.value},
                        "icon": {"type": "string", "default": "🎯"},
                        "descricao": {"type": "string"},
                        "categorias": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["parent_id", "title", "start_time", "duration_minutes"],
                },
            },
            {
                "name": "study_reschedule_section",
                "description": "Reagendar aulas de uma seção (respeita horários de estudo).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "new_start": {"type": "string", "description": "YYYY-MM-DD"},
                        "respect_weekends": {"type": "boolean", "default": True},
                    },
                    "required": ["parent_id", "new_start"],
                },
            },
            {
                "name": "study_query_schedule",
                "description": "Consultar aulas e sessões no período informado.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": STATUS_OPTIONS},
                        "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                        "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 50},
                    },
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Dispatch study tool calls."""
        logger.info("handling_study_tool", tool=tool_name, args=arguments)
        self._ensure_available()

        if tool_name == "study_create_course":
            periodo = self._extract_period(arguments)
            return await self.study_notion.create_card(periodo=periodo, **arguments)

        if tool_name == "study_create_course_complete":
            periodo = self._extract_period(arguments)
            return await self.study_notion.create_course_complete(periodo=periodo, **arguments)

        if tool_name == "study_create_phase":
            periodo = self._extract_period(arguments)
            return await self.study_notion.create_phase(periodo=periodo, **arguments)

        if tool_name == "study_create_section":
            periodo = self._extract_period(arguments)
            return await self.study_notion.create_section(periodo=periodo, **arguments)

        if tool_name == "study_create_class":
            start_time = datetime.fromisoformat(arguments.pop("start_time"))
            duration = arguments.pop("duration_minutes")
            return await self.study_notion.create_class(
                start_time=start_time,
                duration_minutes=duration,
                **arguments,
            )

        if tool_name == "study_reschedule_section":
            new_start = datetime.fromisoformat(arguments.pop("new_start"))
            respect_weekends = arguments.pop("respect_weekends", True)
            return await self.study_notion.reschedule_classes(
                parent_id=arguments["parent_id"],
                new_start_date=new_start,
                respect_weekends=respect_weekends,
            )

        if tool_name == "study_query_schedule":
            return await self.study_notion.query_schedule(**arguments)

        raise ValueError(f"Unknown study tool: {tool_name}")
