"""
YoutuberNotion - Custom implementation for Youtuber database

Handles series and episodes with specific business rules:
- Series period = first recording → last recording
- Episodes have data_lancamento (publication date)
- Recording hours: 21:00-23:50
- Episode 1 has series synopsis
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import structlog

from notion_mcp.custom.base import CustomNotion
from notion_mcp.services.notion_service import NotionService
from notion_mcp.utils import (
    DatabaseType,
    YoutuberStatus,
    create_period,
    format_date_gmt3,
)


logger = structlog.get_logger(__name__)


class YoutuberNotion(CustomNotion):
    """
    Youtuber-specific Notion implementation
    
    Business Rules:
    - Series: No data_lancamento, period = recording schedule
    - Episodes: WITH data_lancamento (publication date)
    - Episode 1: Must have series synopsis in resumo_episodio
    - Recording hours: 21:00-23:50 (default)
    - Relation field: "Item Principal"
    """
    
    RECORDING_START = 21  # 21:00
    RECORDING_END = 23.83  # 23:50
    
    def __init__(self, service: NotionService, database_id: str):
        super().__init__(service, database_id, DatabaseType.YOUTUBER)
    
    def get_default_icon(self) -> str:
        """Default icon for youtuber cards"""
        return "🎬"
    
    async def create_card(
        self,
        title: str,
        status: str = YoutuberStatus.NAO_INICIADO.value,
        periodo: Optional[Dict[str, Any]] = None,
        descricao: Optional[str] = None,
        icon: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create series card
        
        Args:
            title: Series title (without emojis)
            status: Status (default: "Não iniciado")
            periodo: Recording period (first to last episode)
            descricao: Series description
            icon: Emoji icon (default: 🎬)
            **kwargs: Additional properties
        
        Returns:
            Created series page object
        
        Example:
            >>> youtuber = YoutuberNotion(service, database_id)
            >>> series = await youtuber.create_card(
            ...     title="The Legend of Heroes - Trails Series",
            ...     periodo={
            ...         "start": "2025-10-27T21:00:00-03:00",
            ...         "end": "2025-11-30T23:50:00-03:00"
            ...     },
            ...     icon="🎮"
            ... )
        """
        # Validate data
        data = {
            'title': title,
            'status': status,
        }
        if periodo:
            data['periodo'] = periodo
        
        self._validate_and_prepare(data)
        
        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
        }
        
        if periodo:
            properties["Periodo"] = self.service.build_date_property(
                periodo['start'],
                periodo.get('end')
            )
        
        if descricao:
            properties["Descrição"] = self.service.build_rich_text_property(descricao)
        
        # Build icon
        if icon is None:
            icon = self.get_default_icon()
        
        icon_dict = self._get_icon_dict(icon)
        
        logger.info("creating_series", title=title)
        
        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )
    
    async def create_episode(
        self,
        parent_id: str,
        episode_number: int,
        title: str,
        recording_date: datetime,
        publication_date: datetime,
        resumo_episodio: Optional[str] = None,
        status: str = YoutuberStatus.PARA_GRAVAR.value,
        icon: str = "📺",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create episode linked to series
        
        Args:
            parent_id: Series ID
            episode_number: Episode number
            title: Episode title (e.g., "Episódio 01" or custom)
            recording_date: When to record (21:00-23:50)
            publication_date: When to publish (usually next day at 12:00)
            resumo_episodio: Episode description (REQUIRED for episode 1 = series synopsis)
            status: Status (default: "Para Gravar")
            icon: Emoji icon (default: 📺)
            **kwargs: Additional properties
        
        Returns:
            Created episode page object
        
        Example:
            >>> episode = await youtuber.create_episode(
            ...     parent_id=series_id,
            ...     episode_number=1,
            ...     title="Episódio 01",
            ...     recording_date=datetime(2025, 10, 27, 21, 0),
            ...     publication_date=datetime(2025, 10, 28, 12, 0),
            ...     resumo_episodio="Série completa sobre The Legend of Heroes..."
            ... )
        """
        # Validate episode 1 has synopsis
        if episode_number == 1 and not resumo_episodio:
            raise ValueError("Episode 1 must have resumo_episodio (series synopsis)")
        
        # Calculate recording end (default 23:50)
        recording_end = recording_date.replace(hour=23, minute=50, second=0)
        
        # Build period (recording schedule)
        periodo = create_period(recording_date, recording_end, include_time=True)
        
        # Format publication date
        data_lancamento = format_date_gmt3(publication_date, include_time=True)
        
        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Item Principal": self.service.build_relation_property([parent_id]),
            "Periodo": self.service.build_date_property(
                periodo['start'],
                periodo.get('end')
            ),
            "Data de Lançamento": self.service.build_date_property(data_lancamento),
        }
        
        if resumo_episodio:
            properties["Resumo do Episódio"] = self.service.build_rich_text_property(
                resumo_episodio
            )
        
        # Build icon
        icon_dict = self._get_icon_dict(icon)
        
        logger.info(
            "creating_episode",
            parent_id=parent_id,
            episode=episode_number,
            title=title,
            recording=periodo['start'],
            publication=data_lancamento,
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
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generic subitem creation for youtuber database
        
        Args:
            parent_id: Parent series ID
            title: Subitem title
            **kwargs: Additional properties
        
        Returns:
            Created page object
        """
        # This is typically not used directly - prefer create_episode()
        logger.warning(
            "generic_youtuber_subitem",
            message="Use create_episode() instead for better validation"
        )
        
        return await self.create_card(title=title, **kwargs)

