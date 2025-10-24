"""
WorkNotion - Custom implementation for Work database

Handles work projects and tasks with specific business rules:
- Client and Project fields (Astracode, ExpenseIQ, etc)
- Subitems with correct hierarchy
- Work-specific statuses and priorities
"""

from typing import Any, Dict, Optional
import structlog

from notion_mcp.custom.base import CustomNotion
from notion_mcp.services.notion_service import NotionService
from notion_mcp.utils import (
    DatabaseType,
    WorkStatus,
    Priority,
    create_period,
    format_date_gmt3,
)


logger = structlog.get_logger(__name__)


class WorkNotion(CustomNotion):
    """
    Work-specific Notion implementation
    
    Business Rules:
    - Default client: "Astracode"
    - Default project: Based on context
    - Default status: "Não iniciado"
    - Default priority: "Normal"
    - Relation field: "Item Principal"
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
        projeto: Optional[str] = None,
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
            ...     title="Implementar Autenticação JWT",
            ...     projeto="ExpenseIQ",
            ...     prioridade="Alta",
            ...     icon="🔐"
            ... )
        """
        # Validate data
        data = {
            'title': title,
            'status': status,
        }
        self._validate_and_prepare(data)
        
        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Cliente": self.service.build_select_property(cliente),
            "Prioridade": self.service.build_select_property(prioridade),
        }
        
        if projeto:
            properties["Projeto"] = self.service.build_select_property(projeto)
        
        if periodo:
            properties["Periodo"] = self.service.build_date_property(
                periodo['start'],
                periodo.get('end')
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
            'title': title,
            'status': status,
        }
        self._validate_and_prepare(data, parent_id=parent_id)
        
        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Item Principal": self.service.build_relation_property([parent_id]),
            "Prioridade": self.service.build_select_property(prioridade),
        }
        
        if periodo:
            properties["Periodo"] = self.service.build_date_property(
                periodo['start'],
                periodo.get('end')
            )
        
        if tempo_total:
            properties["Tempo Total"] = self.service.build_rich_text_property(tempo_total)
        
        if descricao:
            properties["Descrição"] = self.service.build_rich_text_property(descricao)
        
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
        from notion_mcp.utils.validators import validate_status
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
        properties = {
            "Projeto": self.service.build_select_property(projeto),
        }
        
        logger.info("assigning_to_project", page_id=page_id, projeto=projeto)
        
        return await self.service.update_page(page_id, properties=properties)

