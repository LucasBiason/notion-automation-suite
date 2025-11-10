"""
StudyNotion - Custom implementation for Studies database

Handles courses, phases, sections, and classes with specific business rules:
- Multi-level hierarchy (Course > Phase > Section > Class)
- Study hours respected (19:00-21:00, Tuesday 19:30-21:00)
- Timezone GMT-3 automatic
- Categories and tags
- Time calculations
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import structlog

from notion_mcp.custom.base import CustomNotion
from notion_mcp.services.notion_service import NotionService
from notion_mcp.utils import (
    DatabaseType,
    Priority,
    StudiesStatus,
    create_period,
    enforce_study_hours_limit,
    format_date_gmt3,
    format_duration,
    get_next_business_day,
    get_study_hours,
    parse_duration,
)
from notion_mcp.utils.validators import validate_status

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
        if periodo:
            self._validate_period_without_time(
                periodo,
                "Cursos não aceitam horário. Use create_class para criar aulas com horário específico.",
            )

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

    async def create_course_complete(
        self,
        title: str,
        categorias: Optional[List[str]] = None,
        fases: Optional[List[Dict[str, Any]]] = None,
        periodo: Optional[Dict[str, Any]] = None,
        icon: Optional[str] = None,
        descricao: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a full course with phases, sections, and classes."""

        course = await self.create_card(
            title=title,
            categorias=categorias,
            periodo=periodo,
            descricao=descricao,
            icon=icon,
        )

        created_phases: List[Dict[str, Any]] = []

        for phase_data in fases or []:
            phase_title = phase_data.get("title")
            if not phase_title:
                raise ValueError("Cada fase do curso deve conter um 'title'.")

            phase = await self.create_phase(
                parent_id=course["id"],
                title=phase_title,
                periodo=phase_data.get("periodo"),
                tempo_total=phase_data.get("tempo_total"),
                icon=phase_data.get("icon", "📖"),
                categorias=phase_data.get("categorias"),
                prioridade=phase_data.get("prioridade", Priority.NORMAL.value),
                descricao=phase_data.get("descricao"),
            )

            sections_payload: List[Dict[str, Any]] = []
            for section_data in phase_data.get("sections", []):
                section_title = section_data.get("title")
                if not section_title:
                    raise ValueError(
                        "Cada seção de uma fase deve conter um 'title'."
                    )

                section = await self.create_section(
                    parent_id=phase["id"],
                    title=section_title,
                    periodo=section_data.get("periodo"),
                    tempo_total=section_data.get("tempo_total"),
                    icon=section_data.get("icon", "📑"),
                    categorias=section_data.get("categorias"),
                    prioridade=section_data.get("prioridade", Priority.NORMAL.value),
                    descricao=section_data.get("descricao"),
                )

                classes_payload: List[Dict[str, Any]] = []
                for class_data in section_data.get("classes", []):
                    class_title = class_data.get("title")
                    if not class_title:
                        raise ValueError(
                            "Cada aula precisa ter um 'title' definido."
                        )

                    start_value = class_data.get("start" ) or class_data.get("start_time")
                    if start_value is None:
                        raise ValueError(
                            f"Aula '{class_title}' precisa definir 'start' no formato datetime ou ISO."
                        )

                    start_dt = self._parse_start_datetime(start_value)

                    duration_minutes = int(class_data.get("duration_minutes", 120))

                    class_card = await self.create_class(
                        parent_id=section["id"],
                        title=class_title,
                        start_time=start_dt,
                        duration_minutes=duration_minutes,
                        icon=class_data.get("icon", "🎯"),
                        status=class_data.get("status", StudiesStatus.PARA_FAZER.value),
                        categorias=class_data.get("categorias"),
                        prioridade=class_data.get("prioridade", Priority.NORMAL.value),
                        descricao=class_data.get("descricao"),
                    )

                    classes_payload.append(class_card)

                sections_payload.append({"section": section, "classes": classes_payload})

            created_phases.append({"phase": phase, "sections": sections_payload})

        logger.info(
            "study_course_created",
            title=title,
            phase_count=len(created_phases),
        )

        return {"course": course, "phases": created_phases}

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
        normalized_start, end_time = enforce_study_hours_limit(start_time, duration_minutes)

        periodo = create_period(normalized_start, end_time, include_time=True)
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
            allow_time=True,
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
        allow_time: bool = False,
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

        if periodo and not allow_time:
            self._validate_period_without_time(
                periodo,
                "Fases e seções não devem conter horário. Somente aulas possuem hora definida.",
            )

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

            weekday = current_date.weekday()
            start_hour, _ = get_study_hours(weekday)

            # Set start time
            class_start = current_date.replace(
                hour=int(start_hour), minute=int((start_hour % 1) * 60), second=0
            )

            normalized_start, class_end = enforce_study_hours_limit(class_start, int(duration))

            new_periodo = create_period(normalized_start, class_end, include_time=True)

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
            current_date = get_next_business_day(normalized_start)

        logger.info(
            "rescheduled_classes",
            parent_id=parent_id,
            count=len(updated),
            new_start=format_date_gmt3(new_start_date),
        )

        return updated

    async def query_schedule(
        self,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Query study schedule applying optional filters."""
        filters = []

        if status:
            validate_status(status, self.database_type)
            filters.append({"property": "Status", "status": {"equals": status}})

        if start_date:
            filters.append(
                {
                    "property": "Período",
                    "date": {"on_or_after": start_date},
                }
            )

        if end_date:
            filters.append(
                {
                    "property": "Período",
                    "date": {"on_or_before": end_date},
                }
            )

        filter_payload = {"and": filters} if filters else None
        page_size = max(1, min(limit, 100))

        response = await self.service.query_database(
            database_id=self.database_id,
            filter_conditions=filter_payload,
            sorts=[{"property": "Período", "direction": "ascending"}],
            page_size=page_size,
        )

        return {
            "results": response.get("results", []),
            "has_more": response.get("has_more", False),
            "next_cursor": response.get("next_cursor"),
        }

    @staticmethod
    def _validate_period_without_time(periodo: Dict[str, Any], error_message: str) -> None:
        for key in ("start", "end"):
            value = periodo.get(key)
            if value is None:
                continue

            if isinstance(value, str):
                if "T" in value:
                    raise ValueError(error_message)
            elif isinstance(value, datetime) and (
                value.hour or value.minute or value.second or value.microsecond
            ):
                raise ValueError(error_message)

    @staticmethod
    def _parse_start_datetime(raw_value: Any) -> datetime:
        if isinstance(raw_value, datetime):
            return raw_value

        if isinstance(raw_value, str):
            try:
                return datetime.fromisoformat(raw_value)
            except ValueError as exc:
                raise ValueError(
                    "Datas de início devem estar em formato ISO 8601 (YYYY-MM-DDTHH:MM)."
                ) from exc

        raise TypeError("O campo 'start' da aula deve ser datetime ou string ISO 8601.")

    def _assert_class_schedule(self, start_time: datetime, duration_minutes: int) -> datetime:
        if duration_minutes <= 0:
            raise ValueError("A duração da aula deve ser maior que zero.")

        start_time = start_time.replace(second=0, microsecond=0)

        start_hour, end_hour = get_study_hours(start_time.weekday())
        expected_hour = int(start_hour)
        expected_minute = int((start_hour % 1) * 60)

        if start_time.hour != expected_hour or start_time.minute != expected_minute:
            allowed_label = f"{expected_hour:02d}:{expected_minute:02d}"
            raise ValueError(
                "Aulas devem iniciar exatamente no horário padrão de estudos. "
                f"Para este dia, utilize {allowed_label}."
            )

        available_minutes = int((end_hour - start_hour) * 60)
        if duration_minutes > available_minutes:
            raise ValueError(
                "A duração informada ultrapassa o limite diário (terminaria após 21h00). "
                "Ajuste a carga horária ou reprograme a aula."
            )

        return start_time + timedelta(minutes=duration_minutes)
