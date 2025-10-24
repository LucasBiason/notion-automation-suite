"""
PersonalNotion - Custom implementation for Personal database

Handles personal tasks and events with specific business rules:
- Tarefas principais and subtarefas
- Atividade types
- Simpler status workflow
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import structlog

from notion_mcp.custom.base import CustomNotion
from notion_mcp.services.notion_service import NotionService
from notion_mcp.utils import (
    DatabaseType,
    PersonalStatus,
    create_period,
)

logger = structlog.get_logger(__name__)


class PersonalNotion(CustomNotion):
    """
    Personal-specific Notion implementation

    Business Rules:
    - Simpler workflow (4 statuses only)
    - No priority field
    - Relation field: "Tarefa Principal"
    - Date field name: "Data" (not "Período")
    - Atividade types: Consulta Médica, Pessoal, etc
    """

    def __init__(self, service: NotionService, database_id: str):
        super().__init__(service, database_id, DatabaseType.PERSONAL)

    def get_default_icon(self) -> str:
        """Default icon for personal cards"""
        return "👤"

    async def create_card(
        self,
        title: str,
        status: str = PersonalStatus.NAO_INICIADO.value,
        atividade: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create personal task/event

        Args:
            title: Task title (without emojis)
            status: Personal status (default: "Não iniciado")
            atividade: Activity type (e.g., "Consulta Médica", "Pessoal")
            data: Date period (mapped to "Data" field, not "Período")
            descricao: Description
            icon: Emoji icon (default: 👤)
            **kwargs: Additional properties

        Returns:
            Created page object

        Example:
            >>> personal = PersonalNotion(service, database_id)
            >>> task = await personal.create_card(
            ...     title="Consulta Médica - Dr. Silva",
            ...     atividade="Consulta Médica",
            ...     data={
            ...         "start": "2025-10-25T15:00:00-03:00",
            ...         "end": "2025-10-25T16:00:00-03:00"
            ...     },
            ...     icon="🏥"
            ... )
        """
        # Validate data
        card_data = {
            "title": title,
            "status": status,
        }
        if data:
            card_data["periodo"] = data  # Internally use 'periodo' for validation

        self._validate_and_prepare(card_data)

        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
        }

        if atividade:
            properties["Atividade"] = self.service.build_select_property(atividade)

        # NOTE: Personal database uses "Data" field name (not "Período")
        if data:
            properties["Data"] = self.service.build_date_property(data["start"], data.get("end"))

        if descricao:
            properties["Descrição"] = self.service.build_rich_text_property(descricao)

        # Build icon
        if icon is None:
            icon = self.get_default_icon()

        icon_dict = self._get_icon_dict(icon)

        logger.info(
            "creating_personal_card",
            title=title,
            atividade=atividade,
        )

        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )

    async def create_subitem(
        self,
        parent_id: str,
        title: str,
        status: str = PersonalStatus.NAO_INICIADO.value,
        data: Optional[Dict[str, Any]] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create personal subtask linked to parent task

        Args:
            parent_id: Parent task ID
            title: Subtask title
            status: Personal status (default: "Não iniciado")
            data: Date period
            descricao: Description
            icon: Emoji icon (default: ✅)
            **kwargs: Additional properties

        Returns:
            Created subtask page object
        """
        # Validate data
        card_data = {
            "title": title,
            "status": status,
        }
        if data:
            card_data["periodo"] = data

        self._validate_and_prepare(card_data, parent_id=parent_id)

        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Tarefa Principal": self.service.build_relation_property([parent_id]),
        }

        if data:
            properties["Data"] = self.service.build_date_property(data["start"], data.get("end"))

        if descricao:
            properties["Descrição"] = self.service.build_rich_text_property(descricao)

        # Build icon (default for subtasks)
        if icon is None:
            icon = "✅"

        icon_dict = self._get_icon_dict(icon)

        logger.info(
            "creating_personal_subitem",
            parent_id=parent_id,
            title=title,
        )

        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )

    async def create_medical_appointment(
        self,
        doctor: str,
        specialty: str,
        date: datetime,
        duration_minutes: int = 60,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create medical appointment (template helper)

        Args:
            doctor: Doctor name
            specialty: Medical specialty
            date: Appointment date/time
            duration_minutes: Duration (default: 60 min)
            **kwargs: Additional properties

        Returns:
            Created appointment page object
        """
        title = f"Consulta Médica - Dr. {doctor}"

        end_date = date + timedelta(minutes=duration_minutes)

        data_periodo = create_period(date, end_date, include_time=True)

        descricao = f"Consulta com Dr. {doctor} - {specialty}"

        return await self.create_card(
            title=title,
            atividade="Consulta Médica",
            data=data_periodo,
            descricao=descricao,
            icon="🏥",
            **kwargs,
        )
