"""
Base class for custom Notion implementations

Provides common functionality for all custom Notion classes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import structlog

from services.notion_service import NotionService
from utils import (
    DEFAULT_STATUS,
    DESCRIPTION_FIELD,
    RELATION_FIELD,
    TITLE_FIELD,
    DATE_FIELD,
    DatabaseType,
    validate_card_data,
)

logger = structlog.get_logger(__name__)


class CustomNotion(ABC):
    """
    Base class for custom Notion implementations

    Each subclass implements specific business rules for a database type.

    Attributes:
        service: NotionService instance
        database_id: Database ID for this custom implementation
        database_type: Type of database (WORK, STUDIES, PERSONAL, YOUTUBER)
    """

    def __init__(
        self,
        service: NotionService,
        database_id: str,
        database_type: DatabaseType,
    ):
        """
        Initialize custom Notion implementation

        Args:
            service: NotionService instance
            database_id: Database ID
            database_type: Type of database
        """
        self.service = service
        self.database_id = database_id
        self.database_type = database_type
        self.title_field = TITLE_FIELD[database_type]
        self.relation_field = RELATION_FIELD[database_type]
        self.date_field = DATE_FIELD.get(database_type)
        self.description_field = DESCRIPTION_FIELD.get(database_type)

        logger.info(
            "custom_notion_initialized",
            database_type=database_type.value,
            database_id=database_id,
        )

    @abstractmethod
    async def create_card(
        self,
        title: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a card in this database

        Args:
            title: Card title
            **kwargs: Additional card data

        Returns:
            Created page object

        Raises:
            ValidationError: If data is invalid
        """
        pass

    @abstractmethod
    async def create_subitem(
        self,
        parent_id: str,
        title: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a subitem linked to parent

        Args:
            parent_id: Parent page ID
            title: Subitem title
            **kwargs: Additional card data

        Returns:
            Created page object

        Raises:
            ValidationError: If data is invalid
        """
        pass

    @abstractmethod
    def get_default_icon(self) -> str:
        """
        Get default icon for this database type

        Returns:
            Default emoji icon
        """
        pass

    async def update_card(
        self,
        page_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update a card

        Args:
            page_id: Page ID to update
            **kwargs: Fields to update

        Returns:
            Updated page object
        """
        properties = await self._build_update_properties(**kwargs)

        icon = None
        if "icon" in kwargs or "emoji" in kwargs:
            emoji = kwargs.get("icon") or kwargs.get("emoji")
            icon = {"type": "emoji", "emoji": emoji}

        logger.info("updating_card", page_id=page_id, database_type=self.database_type.value)

        return await self.service.update_page(
            page_id=page_id,
            properties=properties,
            icon=icon,
        )

    async def archive_card(self, page_id: str) -> Dict[str, Any]:
        """
        Archive (soft delete) a card

        Args:
            page_id: Page ID to archive

        Returns:
            Archived page object
        """
        logger.info("archiving_card", page_id=page_id, database_type=self.database_type.value)
        return await self.service.archive_page(page_id)

    async def get_card(self, page_id: str) -> Dict[str, Any]:
        """
        Get card by ID

        Args:
            page_id: Page ID

        Returns:
            Page object
        """
        logger.info("getting_card", page_id=page_id, database_type=self.database_type.value)
        return await self.service.get_page(page_id)

    async def query_cards(
        self,
        filter_conditions: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query cards in this database

        Args:
            filter_conditions: Filter configuration
            sorts: Sort configuration

        Returns:
            List of matching cards
        """
        logger.info(
            "querying_cards",
            database_type=self.database_type.value,
            has_filter=filter_conditions is not None,
        )

        result = await self.service.query_database(
            database_id=self.database_id,
            filter_conditions=filter_conditions,
            sorts=sorts,
        )

        return result.get("results", [])

    def _validate_and_prepare(
        self,
        data: Dict[str, Any],
        parent_id: Optional[str] = None,
    ) -> None:
        """
        Validate card data before creating

        Args:
            data: Card data to validate
            parent_id: Parent page ID (if subitem)

        Raises:
            ValidationError: If validation fails
        """
        validate_card_data(data, self.database_type, parent_id)

    async def _build_properties(
        self,
        title: str,
        status: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Build properties dict for Notion API

        Args:
            title: Card title
            status: Card status
            **kwargs: Additional properties

        Returns:
            Properties dict
        """
        properties: Dict[str, Any] = {
            self.title_field: self.service.build_title_property(title),
        }

        # Add status (use default if not provided)
        if status is None:
            status = DEFAULT_STATUS[self.database_type]

        properties["Status"] = self.service.build_status_property(status)

        # Add parent relation if provided
        if "parent_id" in kwargs and self.relation_field:
            properties[self.relation_field] = self.service.build_relation_property([
                kwargs["parent_id"]
            ])

        return properties

    async def _build_update_properties(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Build properties dict for update operation

        Args:
            **kwargs: Fields to update

        Returns:
            Properties dict for update
        """
        properties: Dict[str, Any] = {}

        if "title" in kwargs:
            properties[self.title_field] = self.service.build_title_property(kwargs["title"])

        if "status" in kwargs:
            properties["Status"] = self.service.build_status_property(kwargs["status"])

        return properties

    def _get_icon_dict(self, emoji: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Build icon dict for Notion API

        Args:
            emoji: Emoji character

        Returns:
            Icon dict or None
        """
        if emoji:
            return {"type": "emoji", "emoji": emoji}
        return None
