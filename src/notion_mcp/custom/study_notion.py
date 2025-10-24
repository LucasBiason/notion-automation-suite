"""
StudyNotion - Custom implementation for Studies database

Handles courses, phases, sections, and classes with specific business rules:
- Multi-level hierarchy (Course > Phase > Section > Class)
- Study hours respected (19:00-21:00, Tuesday 19:30-21:00)
- Timezone GMT-3 automatic
- Categories and tags
- Time calculations
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from notion_mcp.custom.base import CustomNotion
from notion_mcp.services.notion_service import NotionService
from notion_mcp.utils import (
    DatabaseType,
    Priority,
    StudiesStatus,
    calculate_class_end_time,
    create_period,
    format_date_gmt3,
    format_duration,
    get_next_business_day,
    parse_duration,
)

logger = structlog.get_logger(__name__)


class StudyNotion(CustomNotion):
    """
    Studies-specific Notion implementation

    Business Rules:
    - Courses: No time, only dates
    - Phases/Sections: No time, only dates
    - Classes: WITH time (19:00-21:00)
    - Tuesday: Classes start at 19:30 (medical treatment)
    - NEVER after 21:00 (overflow to next day)
    - Categories: FIAP, Rocketseat, Udemy, IA, ML, etc
    """

    def __init__(self, service: NotionService, database_id: str):
        super().__init__(service, database_id, DatabaseType.STUDIES)

    def get_default_icon(self) -> str:
        """Default icon for study cards"""
        return "🎓"

    async def create_card(
        self,
        title: str,
        status: str = StudiesStatus.PARA_FAZER.value,
        categorias: Optional[List[str]] = None,
        prioridade: str = Priority.NORMAL.value,
        periodo: Optional[Dict[str, Any]] = None,
        tempo_total: Optional[str] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create study course/training

        Args:
            title: Course title (without emojis)
            status: Study status (default: "Para Fazer")
            categorias: Category tags (e.g., ["FIAP", "IA"])
            prioridade: Priority (default: "Normal")
            periodo: Period WITHOUT time (courses don't have specific hours)
            tempo_total: Total duration (e.g., "40:00:00" for 40 hours)
            descricao: Description
            icon: Emoji icon (default: 🎓)
            **kwargs: Additional properties

        Returns:
            Created page object

        Example:
            >>> study = StudyNotion(service, database_id)
            >>> course = await study.create_card(
            ...     title="FIAP IA para Devs - Fase 5",
            ...     categorias=["FIAP", "Inteligência Artificial"],
            ...     periodo={"start": "2025-01-15", "end": "2025-03-31"},
            ...     tempo_total="80:00:00",
            ...     icon="🎓"
            ... )
        """
        # Validate data
        data = {
            "title": title,
            "status": status,
        }
        if periodo:
            data["periodo"] = periodo

        self._validate_and_prepare(data)

        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Prioridade": self.service.build_select_property(prioridade),
        }

        if categorias:
            properties["Categorias"] = self.service.build_multi_select_property(categorias)

        if periodo:
            properties["Período"] = self.service.build_date_property(
                periodo["start"], periodo.get("end")
            )

        if tempo_total:
            properties["Tempo Total"] = self.service.build_rich_text_property(tempo_total)

        if descricao:
            properties["Descrição"] = self.service.build_rich_text_property(descricao)

        # Build icon
        if icon is None:
            icon = self.get_default_icon()

        icon_dict = self._get_icon_dict(icon)

        logger.info(
            "creating_study_card",
            title=title,
            categorias=categorias,
            has_time=periodo and "T" in periodo.get("start", "") if periodo else False,
        )

        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )

    async def create_phase(
        self,
        parent_id: str,
        title: str,
        periodo: Optional[Dict[str, Any]] = None,
        tempo_total: Optional[str] = None,
        icon: str = "📖",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create course phase (subitem of course)

        Args:
            parent_id: Course ID
            title: Phase title
            periodo: Period WITHOUT time
            tempo_total: Total duration
            icon: Emoji icon (default: 📖)
            **kwargs: Additional properties

        Returns:
            Created phase page object
        """
        return await self.create_subitem(
            parent_id=parent_id,
            title=title,
            periodo=periodo,
            tempo_total=tempo_total,
            icon=icon,
            **kwargs,
        )

    async def create_section(
        self,
        parent_id: str,
        title: str,
        periodo: Optional[Dict[str, Any]] = None,
        tempo_total: Optional[str] = None,
        icon: str = "📑",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create course section (subitem of phase or course)

        Args:
            parent_id: Phase/Course ID
            title: Section title
            periodo: Period WITHOUT time
            tempo_total: Total duration
            icon: Emoji icon (default: 📑)
            **kwargs: Additional properties

        Returns:
            Created section page object
        """
        return await self.create_subitem(
            parent_id=parent_id,
            title=title,
            periodo=periodo,
            tempo_total=tempo_total,
            icon=icon,
            **kwargs,
        )

    async def create_class(
        self,
        parent_id: str,
        title: str,
        start_time: datetime,
        duration_minutes: int,
        icon: str = "🎯",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create class with correct study hours

        Rules:
        - Default: 19:00-21:00
        - Tuesday: 19:30-21:00
        - If exceeds 21:00, overflow to next business day

        Args:
            parent_id: Section/Course ID
            title: Class title
            start_time: Class start datetime (should be 19:00 or 19:30 on Tuesday)
            duration_minutes: Class duration in minutes
            icon: Emoji icon (default: 🎯)
            **kwargs: Additional properties

        Returns:
            Created class page object

        Example:
            >>> from datetime import datetime
            >>> start = datetime(2025, 10, 22, 19, 0)  # 19:00
            >>> class_card = await study.create_class(
            ...     parent_id=section_id,
            ...     title="Aula 1: Introdução",
            ...     start_time=start,
            ...     duration_minutes=120,  # 2 hours
            ... )
        """
        # Calculate end time (respecting 21:00 limit)
        end_time = calculate_class_end_time(start_time, duration_minutes)

        # Format times to GMT-3
        periodo = create_period(start_time, end_time, include_time=True)

        # Calculate tempo_total
        tempo_total = format_duration(duration_minutes)

        logger.info(
            "creating_class",
            title=title,
            start=periodo["start"],
            end=periodo["end"],
            duration=tempo_total,
        )

        return await self.create_subitem(
            parent_id=parent_id,
            title=title,
            periodo=periodo,
            tempo_total=tempo_total,
            icon=icon,
            **kwargs,
        )

    async def create_subitem(
        self,
        parent_id: str,
        title: str,
        status: str = StudiesStatus.PARA_FAZER.value,
        categorias: Optional[List[str]] = None,
        prioridade: str = Priority.NORMAL.value,
        periodo: Optional[Dict[str, Any]] = None,
        tempo_total: Optional[str] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create study subitem linked to parent

        Args:
            parent_id: Parent course/phase/section ID
            title: Subitem title
            status: Study status (default: "Para Fazer")
            categorias: Category tags
            prioridade: Priority (default: "Normal")
            periodo: Period dict
            tempo_total: Total duration
            descricao: Description
            icon: Emoji icon (default: 📑)
            **kwargs: Additional properties

        Returns:
            Created subitem page object
        """
        # Validate data
        data = {
            "title": title,
            "status": status,
        }
        if periodo:
            data["periodo"] = periodo

        self._validate_and_prepare(data, parent_id=parent_id)

        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Item Principal": self.service.build_relation_property([parent_id]),
            "Prioridade": self.service.build_select_property(prioridade),
        }

        if categorias:
            properties["Categorias"] = self.service.build_multi_select_property(categorias)

        if periodo:
            properties["Período"] = self.service.build_date_property(
                periodo["start"], periodo.get("end")
            )

        if tempo_total:
            properties["Tempo Total"] = self.service.build_rich_text_property(tempo_total)

        if descricao:
            properties["Descrição"] = self.service.build_rich_text_property(descricao)

        # Build icon
        if icon is None:
            icon = "📑"

        icon_dict = self._get_icon_dict(icon)

        logger.info(
            "creating_study_subitem",
            parent_id=parent_id,
            title=title,
        )

        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )

    async def reschedule_classes(
        self,
        parent_id: str,
        new_start_date: datetime,
        respect_weekends: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Reschedule all classes of a section/course

        Args:
            parent_id: Section/Course ID
            new_start_date: New start date
            respect_weekends: Skip Saturday/Sunday

        Returns:
            List of updated class pages
        """
        # Query all classes (subitems)
        filter_conditions = {
            "property": "Item Principal",
            "relation": {"contains": parent_id},
        }

        classes = await self.query_cards(filter_conditions=filter_conditions)

        # Sort by original start date
        classes.sort(
            key=lambda c: c.get("properties", {})
            .get("Período", {})
            .get("date", {})
            .get("start", "")
        )

        updated = []
        current_date = new_start_date

        for class_card in classes:
            # Get duration
            props = class_card.get("properties", {})
            tempo_total = (
                props.get("Tempo Total", {})
                .get("rich_text", [{}])[0]
                .get("text", {})
                .get("content", "01:00:00")
            )
            duration = parse_duration(tempo_total)

            # Calculate new period
            from notion_mcp.utils.formatters import get_study_hours

            weekday = current_date.weekday()
            start_hour, _ = get_study_hours(weekday)

            # Set start time
            class_start = current_date.replace(
                hour=int(start_hour), minute=int((start_hour % 1) * 60), second=0
            )

            class_end = calculate_class_end_time(class_start, int(duration))

            # Update class
            new_periodo = create_period(class_start, class_end, include_time=True)

            updated_page = await self.service.update_page(
                page_id=class_card["id"],
                properties={
                    "Período": self.service.build_date_property(
                        new_periodo["start"], new_periodo.get("end")
                    )
                },
            )

            updated.append(updated_page)

            # Next class on next business day
            current_date = get_next_business_day(class_end)

        logger.info(
            "rescheduled_classes",
            parent_id=parent_id,
            count=len(updated),
            new_start=format_date_gmt3(new_start_date),
        )

        return updated
