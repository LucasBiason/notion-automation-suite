"""
PersonalNotion - Custom implementation for Personal database

Handles personal tasks and events with specific business rules:
- Tarefas principais and subtarefas
- Atividade types
- Simpler status workflow
"""

import calendar
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import structlog

from .base import CustomNotion
from services.notion_service import NotionService
from utils import (
    DATE_FIELD,
    DESCRIPTION_FIELD,
    RELATION_FIELD,
    TITLE_FIELD,
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
    - Date field name: "Data" (Notion property name)
    - Activity types: Medical Appointment, Personal, etc.
    """

    TEMPLATES: Dict[str, Dict[str, Any]] = {
        "weekly_planning": {
            "title": "Planejamento Semanal",
            "atividade": "Planejamento",
            "icon": "🗓️",
            "weekday": 0,
            "start_hour": 7,
            "duration_minutes": 120,
            "descricao": "Sessão de planejamento semanal.",
        },
        "health_session": {
            "title": "Sessão de Saúde",
            "atividade": "Saúde",
            "icon": "💪",
            "weekday": 1,
            "start_hour": 7.5,
            "duration_minutes": 60,
            "descricao": "Rotina de saúde ou treino.",
        },
        "invoice_routine": {
            "title": "Emissão de Nota Fiscal",
            "atividade": "Financeiro",
            "icon": "💸",
            "monthly_day": 1,
            "include_time": False,
            "descricao": "Preparar e enviar a NF do mês.",
        },
        "financial_review_weekly": {
            "title": "Revisão Financeira (Semanal)",
            "atividade": "Financeiro",
            "icon": "📊",
            "weekday": 4,
            "start_hour": 8,
            "duration_minutes": 45,
            "descricao": "Acompanhamento financeiro da semana.",
        },
        "financial_review_monthly": {
            "title": "Revisão Financeira (Mensal)",
            "atividade": "Financeiro",
            "icon": "📝",
            "monthly_day": 28,
            "include_time": False,
            "descricao": "Revisão financeira do mês.",
        },
    }

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
            status: Personal status label (default Notion value "Não iniciado")
            atividade: Activity type (e.g., "Consulta Médica", "Pessoal")
            data: Date period (mapped to Notion property "Data")
            descricao: Description
            icon: Emoji icon (default: 👤)
            **kwargs: Additional properties

        Returns:
            Created page object

        Example:
            >>> personal = PersonalNotion(service, database_id)
            >>> task = await personal.create_card(
            ...     title="Medical Check-up - Dr. Silva",
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
            self.title_field: self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
        }

        if atividade:
            properties["Atividade"] = self.service.build_select_property(atividade)

        if data and self.date_field:
            properties[self.date_field] = self.service.build_date_property(
                data["start"], data.get("end")
            )

        if descricao and self.description_field:
            properties[self.description_field] = self.service.build_rich_text_property(descricao)

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
            status: Personal status label (default Notion value "Não iniciado")
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
            self.title_field: self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            self.relation_field: self.service.build_relation_property([parent_id]),
        }

        if data and self.date_field:
            properties[self.date_field] = self.service.build_date_property(
                data["start"], data.get("end")
            )

        if descricao and self.description_field:
            properties[self.description_field] = self.service.build_rich_text_property(descricao)

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

    async def use_template(
        self,
        template_name: str,
        reference_date: datetime,
        overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a personal card based on a predefined generic template."""

        template = self.TEMPLATES.get(template_name)
        if template is None:
            raise ValueError(f"Unknown personal template: {template_name}")

        payload: Dict[str, Any] = {**template}
        if overrides:
            payload.update(overrides)

        schedule = self._build_template_schedule(payload, reference_date)

        descricao = payload.get("descricao")

        return await self.create_card(
            title=payload["title"],
            atividade=payload.get("atividade"),
            status=payload.get("status", PersonalStatus.NAO_INICIADO.value),
            data=schedule,
            descricao=descricao,
            icon=payload.get("icon", self.get_default_icon()),
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
        title = f"Consulta com {doctor} ({specialty})"

        end_date = date + timedelta(minutes=duration_minutes)

        data_periodo = create_period(date, end_date, include_time=True)

        descricao = f"Atendimento com {doctor} ({specialty})."

        return await self.create_card(
            title=title,
            atividade="Consulta Médica",
            data=data_periodo,
            descricao=descricao,
            icon="🏥",
            **kwargs,
        )

    def _build_template_schedule(
        self,
        template: Dict[str, Any],
        reference_date: datetime,
    ) -> Dict[str, Any]:
        if "weekday" in template:
            target_date = self._resolve_weekday_date(reference_date, int(template["weekday"]))
            start_hour = template.get("start_hour", 0)
            duration = int(template.get("duration_minutes", 60))
            if duration <= 0:
                raise ValueError(
                    "Weekly templates must provide 'duration_minutes' greater than zero."
                )
            start_datetime = target_date.replace(
                hour=int(start_hour),
                minute=int((start_hour % 1) * 60),
                second=0,
                microsecond=0,
            )
            end_datetime = start_datetime + timedelta(minutes=duration)
            return create_period(start_datetime, end_datetime, include_time=True)

        if "monthly_day" in template:
            target_date = self._resolve_monthly_date(reference_date, int(template["monthly_day"]))
            include_time = template.get("include_time", False)
            if include_time:
                start_hour = template.get("start_hour", 9)
                start_datetime = target_date.replace(
                    hour=int(start_hour),
                    minute=int((start_hour % 1) * 60),
                    second=0,
                    microsecond=0,
                )
                duration = int(template.get("duration_minutes", 60))
                if duration <= 0:
                    raise ValueError(
                        "Templates with schedules must provide 'duration_minutes' greater than zero."
                    )
                end_datetime = start_datetime + timedelta(minutes=duration)
                return create_period(start_datetime, end_datetime, include_time=True)

            target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            return create_period(target_date, include_time=False)

        raise ValueError("Template is missing scheduling details (weekday or monthly_day)")

    @staticmethod
    def _resolve_weekday_date(reference: datetime, weekday: int) -> datetime:
        base = reference.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = (weekday - base.weekday()) % 7
        return base + timedelta(days=delta)

    @staticmethod
    def _resolve_monthly_date(reference: datetime, day: int) -> datetime:
        year = reference.year
        month = reference.month
        last_day = calendar.monthrange(year, month)[1]
        clamped_day = min(max(1, day), last_day)
        return datetime(year, month, clamped_day)
