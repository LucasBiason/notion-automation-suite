"""
Work Notion MCP Tools

Provides specialized tools for work database operations.
"""
from typing import Any, Dict, List

import structlog

from notion_mcp.utils.constants import WORK_CLIENTS, WORK_PROJECTS, Priority, WorkStatus

logger = structlog.get_logger(__name__)

PRIORITY_OPTIONS = [priority.value for priority in Priority]
STATUS_OPTIONS = [status.value for status in WorkStatus]


class WorkNotionTools:
    """Tools for work database operations"""

    def __init__(self, work_notion):
        self.work_notion = work_notion

    def _ensure_available(self) -> None:
        if self.work_notion is None:
            raise ValueError(
                "Work database is not configured for this MCP server. Configure NOTION_WORK_DATABASE_ID first."
            )

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return tool metadata for the work database."""
        return [
            {
                "name": "work_create_project",
                "description": "Criar projeto de trabalho com cliente, projeto e prioridade corretos.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Título do projeto (sem emojis).",
                        },
                        "cliente": {
                            "type": "string",
                            "enum": WORK_CLIENTS,
                            "default": WORK_CLIENTS[0],
                        },
                        "projeto": {
                            "type": "string",
                            "enum": WORK_PROJECTS,
                            "description": "Projeto vinculado (ExpenseIQ, HubTravel, Avulso).",
                        },
                        "prioridade": {
                            "type": "string",
                            "enum": PRIORITY_OPTIONS,
                            "default": Priority.NORMAL.value,
                        },
                        "status": {
                            "type": "string",
                            "enum": STATUS_OPTIONS,
                            "default": WorkStatus.NAO_INICIADO.value,
                        },
                        "periodo": {
                            "type": "object",
                            "description": "Período planejado (start/end em ISO-8601 GMT-3).",
                        },
                        "tempo_total": {
                            "type": "string",
                            "description": "Estimativa de duração (ex: '08:00:00' para 8h).",
                        },
                        "descricao": {"type": "string"},
                        "icon": {
                            "type": "string",
                            "description": "Emoji para o card (ex: 🚀).",
                        },
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "work_create_sprint",
                "description": "Criar sprint com projeto e subtarefas opcionais de forma padronizada.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "cliente": {
                            "type": "string",
                            "enum": WORK_CLIENTS,
                            "default": WORK_CLIENTS[0],
                        },
                        "projeto": {
                            "type": "string",
                            "enum": WORK_PROJECTS,
                            "default": WORK_PROJECTS[0],
                        },
                        "prioridade": {
                            "type": "string",
                            "enum": PRIORITY_OPTIONS,
                            "default": Priority.NORMAL.value,
                        },
                        "status": {
                            "type": "string",
                            "enum": STATUS_OPTIONS,
                            "default": WorkStatus.NAO_INICIADO.value,
                        },
                        "periodo": {"type": "object"},
                        "descricao": {"type": "string"},
                        "icon": {"type": "string"},
                        "tasks": {
                            "type": "array",
                            "description": "Lista de tarefas da sprint.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "status": {"type": "string", "enum": STATUS_OPTIONS},
                                    "prioridade": {
                                        "type": "string",
                                        "enum": PRIORITY_OPTIONS,
                                        "default": Priority.NORMAL.value,
                                    },
                                    "periodo": {"type": "object"},
                                    "tempo_total": {"type": "string"},
                                    "descricao": {"type": "string"},
                                    "icon": {"type": "string"},
                                },
                                "required": ["title"],
                            },
                        },
                    },
                    "required": ["title", "projeto"],
                },
            },
            {
                "name": "work_create_task",
                "description": "Criar tarefa/subitem vinculado a um projeto ou sprint.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "title": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": STATUS_OPTIONS,
                            "default": WorkStatus.NAO_INICIADO.value,
                        },
                        "prioridade": {
                            "type": "string",
                            "enum": PRIORITY_OPTIONS,
                            "default": Priority.NORMAL.value,
                        },
                        "periodo": {"type": "object"},
                        "tempo_total": {"type": "string"},
                        "descricao": {"type": "string"},
                        "icon": {"type": "string"},
                    },
                    "required": ["parent_id", "title"],
                },
            },
            {
                "name": "work_update_status",
                "description": "Atualizar status de um item de trabalho (projeto, sprint ou tarefa).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "status": {"type": "string", "enum": STATUS_OPTIONS},
                    },
                    "required": ["page_id", "status"],
                },
            },
            {
                "name": "work_assign_project",
                "description": "Alterar o projeto vinculado a um card existente.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "projeto": {"type": "string", "enum": WORK_PROJECTS},
                    },
                    "required": ["page_id", "projeto"],
                },
            },
            {
                "name": "work_query_projects",
                "description": "Consultar cards de trabalho por status, cliente ou projeto.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": STATUS_OPTIONS},
                        "cliente": {"type": "string", "enum": WORK_CLIENTS},
                        "projeto": {"type": "string", "enum": WORK_PROJECTS},
                        "limit": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100,
                            "default": 25,
                        },
                    },
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute WorkNotion tool calls."""
        logger.info("handling_work_tool", tool=tool_name, args=arguments)
        self._ensure_available()

        if tool_name == "work_create_project":
            return await self.work_notion.create_card(**arguments)

        if tool_name == "work_create_sprint":
            return await self.work_notion.create_sprint(**arguments)

        if tool_name == "work_create_task":
            return await self.work_notion.create_task(**arguments)

        if tool_name == "work_update_status":
            return await self.work_notion.update_status(**arguments)

        if tool_name == "work_assign_project":
            return await self.work_notion.assign_to_project(**arguments)

        if tool_name == "work_query_projects":
            return await self.work_notion.query_projects(**arguments)

        raise ValueError(f"Unknown work tool: {tool_name}")
