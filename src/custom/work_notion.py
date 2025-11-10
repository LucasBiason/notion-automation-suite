"""
WorkNotion - Custom implementation for Work database

Handles work projects and tasks with specific business rules:
- Client and Project fields (Astracode, ExpenseIQ, etc)
- Subitems with correct hierarchy
- Work-specific statuses and priorities
"""

from typing import Any, Dict, List, Optional

import structlog

from .base import CustomNotion
from services.notion_service import NotionService
from utils import (
    DATE_FIELD,
    DESCRIPTION_FIELD,
    RELATION_FIELD,
    TITLE_FIELD,
    DatabaseType,
    Priority,
    WorkStatus,
    WORK_CLIENTS,
    WORK_PROJECTS,
)
from utils.validators import validate_status

logger = structlog.get_logger(__name__)


class WorkNotion(CustomNotion):
    """
    Work-specific Notion implementation

    Business Rules:
    - Default client: "Astracode"
    - Default project: Based on context
    - Default status label: "Não iniciado"
    - Default priority: "Normal"
    - Relation field: "item principal"
    """

    def __init__(self, service: NotionService, database_id: str):
        super().__init__(service, database_id, DatabaseType.WORK)

    def get_default_icon(self) -> str:
        """Default icon for work cards"""
        return "🚀"

    async def create_card(
        self,
        title: str,
        status: str = WorkStatus.NAO_INICIADO.value,
        cliente: str = "Astracode",
        projeto: Optional[str] = "Avulso",
        prioridade: str = Priority.NORMAL.value,
        periodo: Optional[Dict[str, Any]] = None,
        tempo_total: Optional[str] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create work project or task

        Args:
            title: Project/task title (without emojis)
            status: Work status (default: "Não iniciado")
            cliente: Client name (default: "Astracode")
            projeto: Project name (e.g., "ExpenseIQ", "HubTravel")
            prioridade: Priority (default: "Normal")
            periodo: Period dict with start/end dates
            tempo_total: Total time estimate
            descricao: Description
            icon: Emoji icon (default: 🚀)
            **kwargs: Additional properties

        Returns:
            Created page object

        Example:
            >>> work = WorkNotion(service, database_id)
            >>> card = await work.create_card(
            ...     title="Implement JWT authentication",
            ...     projeto="ExpenseIQ",
            ...     prioridade="Alta",
            ...     icon="🔐"
            ... )
        """
        # Validate data
        data = {
            "title": title,
            "status": status,
        }
        self._validate_and_prepare(data)
        self._validate_cliente(cliente)
        if projeto:
            self._validate_projeto(projeto)

        # Build properties
        properties = {
            self.title_field: self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Cliente": self.service.build_select_property(cliente),
            "Prioridade": self.service.build_select_property(prioridade),
        }

        if projeto:
            properties["Projeto"] = self.service.build_select_property(projeto)

        if periodo and self.date_field:
            properties[self.date_field] = self.service.build_date_property(
                periodo["start"], periodo.get("end")
            )

        if tempo_total:
            logger.warning(
                "work_ignoring_tempo_total",
                reason="No 'Tempo Total' field configured for the work database",
            )

        if descricao:
            logger.warning(
                "work_ignoring_descricao",
                reason="No descriptive field configured for the work database",
            )

        # Build icon
        if icon is None:
            icon = self.get_default_icon()

        icon_dict = self._get_icon_dict(icon)

        logger.info(
            "creating_work_card",
            title=title,
            cliente=cliente,
            projeto=projeto,
        )

        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )

    async def create_task(
        self,
        parent_id: str,
        title: str,
        status: str = WorkStatus.NAO_INICIADO.value,
        prioridade: str = Priority.NORMAL.value,
        periodo: Optional[Dict[str, Any]] = None,
        tempo_total: Optional[str] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Wrapper for create_subitem, kept for tool clarity."""
        return await self.create_subitem(
            parent_id=parent_id,
            title=title,
            status=status,
            prioridade=prioridade,
            periodo=periodo,
            tempo_total=tempo_total,
            descricao=descricao,
            icon=icon,
            **kwargs,
        )

    async def create_subitem(
        self,
        parent_id: str,
        title: str,
        status: str = WorkStatus.NAO_INICIADO.value,
        prioridade: str = Priority.NORMAL.value,
        periodo: Optional[Dict[str, Any]] = None,
        tempo_total: Optional[str] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create work subitem linked to parent

        Args:
            parent_id: Parent project/task ID
            title: Subitem title
            status: Work status (default: "Não iniciado")
            prioridade: Priority (default: "Normal")
            periodo: Period dict with start/end dates
            tempo_total: Total time estimate
            descricao: Description
            icon: Emoji icon (default: 📋)
            **kwargs: Additional properties

        Returns:
            Created subitem page object

        Example:
            >>> subitem = await work.create_subitem(
            ...     parent_id=project_id,
            ...     title="Implementar Login Endpoint",
            ...     prioridade="Alta"
            ... )
        """
        # Validate data
        data = {
            "title": title,
            "status": status,
        }
        self._validate_and_prepare(data, parent_id=parent_id)

        # Build properties
        properties = {
            self.title_field: self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            self.relation_field: self.service.build_relation_property([parent_id]),
            "Prioridade": self.service.build_select_property(prioridade),
        }

        if periodo and self.date_field:
            properties[self.date_field] = self.service.build_date_property(
                periodo["start"], periodo.get("end")
            )

        if tempo_total:
            logger.warning(
                "work_subitem_ignoring_tempo_total",
                reason="No 'Tempo Total' field configured for the work database",
            )

        if descricao:
            logger.warning(
                "work_subitem_ignoring_descricao",
                reason="No descriptive field configured for the work database",
            )

        # Build icon (default for subitems)
        if icon is None:
            icon = "📋"

        icon_dict = self._get_icon_dict(icon)

        logger.info(
            "creating_work_subitem",
            parent_id=parent_id,
            title=title,
        )

        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )

    async def create_sprint(
        self,
        title: str,
        cliente: str = "Astracode",
        projeto: str = "Avulso",
        prioridade: str = Priority.NORMAL.value,
        periodo: Optional[Dict[str, Any]] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        tasks: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Create a sprint card and optional task subitems."""

        sprint = await self.create_card(
            title=title,
            cliente=cliente,
            projeto=projeto,
            prioridade=prioridade,
            periodo=periodo,
            descricao=descricao,
            icon=icon,
        )

        created_tasks: List[Dict[str, Any]] = []
        if tasks:
            parent_id = sprint["id"]
            for task in tasks:
                task_title = task.get("title")
                if not task_title:
                    raise ValueError("Each task registered in a sprint must include a 'title'")

                task_status = task.get("status", WorkStatus.NAO_INICIADO.value)
                task_priority = task.get("prioridade", Priority.NORMAL.value)
                task_periodo = task.get("periodo")
                task_tempo_total = task.get("tempo_total")
                task_descricao = task.get("descricao")
                task_icon = task.get("icon")

                created_task = await self.create_subitem(
                    parent_id=parent_id,
                    title=task_title,
                    status=task_status,
                    prioridade=task_priority,
                    periodo=task_periodo,
                    tempo_total=task_tempo_total,
                    descricao=task_descricao,
                    icon=task_icon,
                )
                created_tasks.append(created_task)

        logger.info(
            "work_sprint_created",
            title=title,
            task_count=len(created_tasks),
        )

        return {"sprint": sprint, "tasks": created_tasks}

    async def update_status(
        self,
        page_id: str,
        status: str,
    ) -> Dict[str, Any]:
        """
        Update card status

        Args:
            page_id: Page ID
            status: New status

        Returns:
            Updated page object
        """
        # Validate status
        validate_status(status, self.database_type)

        logger.info("updating_work_status", page_id=page_id, status=status)

        return await self.update_card(page_id, status=status)

    async def assign_to_project(
        self,
        page_id: str,
        projeto: str,
    ) -> Dict[str, Any]:
        """
        Assign card to project

        Args:
            page_id: Page ID
            projeto: Project name

        Returns:
            Updated page object
        """
        self._validate_projeto(projeto)

        properties = {
            "Projeto": self.service.build_select_property(projeto),
        }

        logger.info("assigning_to_project", page_id=page_id, projeto=projeto)

        return await self.service.update_page(page_id, properties=properties)

    async def query_projects(
        self,
        status: Optional[str] = None,
        cliente: Optional[str] = None,
        projeto: Optional[str] = None,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Query work projects applying business filters."""
        filters = []

        if status:
            validate_status(status, self.database_type)
            filters.append({"property": "Status", "status": {"equals": status}})

        if cliente:
            self._validate_cliente(cliente)
            filters.append({"property": "Cliente", "select": {"equals": cliente}})

        if projeto:
            self._validate_projeto(projeto)
            filters.append({"property": "Projeto", "select": {"equals": projeto}})

        filter_payload = {"and": filters} if filters else None
        page_size = max(1, min(limit, 100))

        response = await self.service.query_database(
            database_id=self.database_id,
            filter_conditions=filter_payload,
            page_size=page_size,
        )

        return {
            "results": response.get("results", []),
            "has_more": response.get("has_more", False),
            "next_cursor": response.get("next_cursor"),
        }

    @staticmethod
    def _validate_cliente(cliente: str) -> None:
        if cliente not in WORK_CLIENTS:
            raise ValueError(
                "Invalid client for the work database. Accepted values: "
                f"{', '.join(WORK_CLIENTS)}"
            )

    @staticmethod
    def _validate_projeto(projeto: str) -> None:
        if projeto not in WORK_PROJECTS:
            raise ValueError(
                "Invalid project value for the work database. Accepted values: "
                f"{', '.join(WORK_PROJECTS)}"
            )
