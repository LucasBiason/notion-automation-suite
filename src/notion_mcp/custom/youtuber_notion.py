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
from notion_mcp.utils.validators import validate_status

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

    async def create_series(
        self,
        title: str,
        sinopse: str,
        total_episodes: int,
        first_recording: datetime,
        recording_interval_days: int = 1,
        publication_hour: int = 12,
        icon: Optional[str] = None,
        episodes: Optional[list] = None,
    ) -> Dict[str, Any]:
        """Create a full series with automatically scheduled episodes."""

        if total_episodes <= 0:
            raise ValueError("Uma série precisa ter pelo menos um episódio")

        normalized_first = self._normalize_recording_start(first_recording)

        episodes_payload = self._build_episode_schedule(
            total_episodes=total_episodes,
            first_recording=normalized_first,
            recording_interval_days=recording_interval_days,
            publication_hour=publication_hour,
            sinopse=sinopse,
            overrides=episodes or [],
        )

        last_recording = episodes_payload[-1]["recording_date"].replace(
            hour=23, minute=50, second=0, microsecond=0
        )
        periodo = create_period(normalized_first, last_recording, include_time=True)

        series_card = await self.create_card(
            title=title,
            periodo=periodo,
            descricao=sinopse,
            icon=icon,
        )

        created_episodes = []
        for episode_number, payload in enumerate(episodes_payload, start=1):
            resumo = payload.get("resumo_episodio") if episode_number > 1 else sinopse
            episode_title = payload.get("title") or f"Episódio {episode_number:02d}"

            created = await self.create_episode(
                parent_id=series_card["id"],
                episode_number=episode_number,
                title=episode_title,
                recording_date=payload["recording_date"],
                publication_date=payload["publication_date"],
                resumo_episodio=resumo,
                status=payload.get("status", YoutuberStatus.PARA_GRAVAR.value),
                icon=payload.get("icon", "📺"),
            )
            created_episodes.append(created)

        logger.info(
            "series_created",
            title=title,
            episodes=len(created_episodes),
        )

        return {"series": series_card, "episodes": created_episodes}

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
        }

        if periodo:
            properties["Periodo"] = self.service.build_date_property(
                periodo["start"], periodo.get("end")
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

        recording_start = self._normalize_recording_start(recording_date)
        recording_end = recording_start.replace(hour=23, minute=50, second=0, microsecond=0)

        periodo = create_period(recording_start, recording_end, include_time=True)

        self._validate_publication_after_recording(recording_end, publication_date)
        data_lancamento = format_date_gmt3(publication_date, include_time=True)

        # Build properties
        properties = {
            "Project name": self.service.build_title_property(title),
            "Status": self.service.build_status_property(status),
            "Item Principal": self.service.build_relation_property([parent_id]),
            "Periodo": self.service.build_date_property(periodo["start"], periodo.get("end")),
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
            recording=periodo["start"],
            publication=data_lancamento,
        )

        return await self.service.create_page(
            database_id=self.database_id,
            properties=properties,
            icon=icon_dict,
        )

    async def update_episode_status(
        self,
        episode_id: str,
        status: str,
    ) -> Dict[str, Any]:
        """Update episode status."""
        validate_status(status, self.database_type)
        logger.info("youtuber_update_status", episode_id=episode_id, status=status)
        properties = {"Status": self.service.build_status_property(status)}
        return await self.service.update_page(episode_id, properties=properties)

    async def reschedule_episode(
        self,
        episode_id: str,
        new_recording_date: Optional[datetime] = None,
        new_publication_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Reschedule recording and/or publication for an episode."""
        if new_recording_date is None and new_publication_date is None:
            raise ValueError("Informe ao menos uma nova data de gravação ou publicação")

        properties: Dict[str, Any] = {}

        if new_recording_date is not None:
            normalized_start = self._normalize_recording_start(new_recording_date)
            recording_end = normalized_start.replace(hour=23, minute=50, second=0, microsecond=0)
            periodo = create_period(normalized_start, recording_end, include_time=True)
            properties["Periodo"] = self.service.build_date_property(
                periodo["start"], periodo.get("end")
            )

        if new_publication_date is not None:
            properties["Data de Lançamento"] = self.service.build_date_property(
                format_date_gmt3(new_publication_date, include_time=True)
            )

        if not properties:
            raise ValueError("Nenhuma atualização aplicada ao episódio")

        logger.info("youtuber_reschedule_episode", episode_id=episode_id, has_recording=new_recording_date is not None, has_publication=new_publication_date is not None)
        return await self.service.update_page(episode_id, properties=properties)

    async def schedule_recordings(
        self,
        series_id: str,
        total_episodes: int,
        start_recording: datetime,
        recording_interval_days: int = 1,
        publication_hour: int = 12,
        base_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a block of episodes for an existing series."""
        if total_episodes <= 0:
            raise ValueError("total_episodes deve ser maior que zero")

        normalized_start = self._normalize_recording_start(start_recording)
        titles_base = base_title or "Episódio"
        created: List[Dict[str, Any]] = []

        for index in range(total_episodes):
            episode_number = index + 1
            recording_date = normalized_start + timedelta(days=index * recording_interval_days)
            recording_start = self._normalize_recording_start(recording_date)
            publication_date = (recording_start + timedelta(days=1)).replace(
                hour=publication_hour, minute=0, second=0, microsecond=0
            )
            title = f"{titles_base} {episode_number:02d}"
            created_episode = await self.create_episode(
                parent_id=series_id,
                episode_number=episode_number,
                title=title,
                recording_date=recording_start,
                publication_date=publication_date,
            )
            created.append(created_episode)

        return {"episodes": created, "count": len(created)}

    async def query_schedule(
        self,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Query episodes filtered by status and/or period."""
        filters = []

        if status:
            validate_status(status, self.database_type)
            filters.append({"property": "Status", "status": {"equals": status}})

        if start_date:
            filters.append({"property": "Data de Lançamento", "date": {"on_or_after": start_date}})

        if end_date:
            filters.append({"property": "Data de Lançamento", "date": {"on_or_before": end_date}})

        filter_payload = {"and": filters} if filters else None
        page_size = max(1, min(limit, 100))

        response = await self.service.query_database(
            database_id=self.database_id,
            filter_conditions=filter_payload,
            sorts=[{"property": "Data de Lançamento", "direction": "ascending"}],
            page_size=page_size,
        )

        return {
            "results": response.get("results", []),
            "has_more": response.get("has_more", False),
            "next_cursor": response.get("next_cursor"),
        }

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
            "generic_youtuber_subitem", message="Use create_episode() instead for better validation"
        )

        return await self.create_card(title=title, **kwargs)

    def _build_episode_schedule(
        self,
        total_episodes: int,
        first_recording: datetime,
        recording_interval_days: int,
        publication_hour: int,
        sinopse: str,
        overrides: list,
    ) -> list:
        payload = []

        for index in range(total_episodes):
            episode_number = index + 1
            override = overrides[index] if index < len(overrides) else {}

            recording_date_raw = override.get("recording_date") or override.get("recording_start")
            if recording_date_raw is not None:
                recording_date = self._parse_datetime(recording_date_raw)
            else:
                recording_date = first_recording + timedelta(days=index * recording_interval_days)

            recording_date = self._normalize_recording_start(recording_date)

            publication_raw = override.get("publication_date")
            if publication_raw is not None:
                publication_date = self._parse_datetime(publication_raw)
            else:
                publication_date = self._default_publication_date(recording_date, publication_hour)

            payload.append(
                {
                    "recording_date": recording_date,
                    "publication_date": publication_date,
                    "title": override.get("title"),
                    "resumo_episodio": override.get("resumo_episodio", sinopse if episode_number == 1 else None),
                    "status": override.get("status"),
                    "icon": override.get("icon"),
                }
            )

        return payload

    @staticmethod
    def _parse_datetime(value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError as exc:
                raise ValueError(
                    "Datas de gravação/publicação devem estar em formato ISO 8601 (YYYY-MM-DDTHH:MM)."
                ) from exc

        raise TypeError("Datas de gravação/publicação devem ser datetime ou string ISO 8601.")

    def _normalize_recording_start(self, recording_start: datetime) -> datetime:
        expected_hour = int(self.RECORDING_START)
        expected_minute = int((self.RECORDING_START % 1) * 60)

        normalized = recording_start.replace(second=0, microsecond=0)

        if normalized.hour != expected_hour or normalized.minute != expected_minute:
            raise ValueError(
                "Gravações devem iniciar às 21h00 para manter a rotina do canal."
            )

        return normalized

    @staticmethod
    def _default_publication_date(recording_date: datetime, publication_hour: int) -> datetime:
        publication_hour = max(0, min(23, publication_hour))
        return (recording_date + timedelta(days=1)).replace(
            hour=publication_hour, minute=0, second=0, microsecond=0
        )

    @staticmethod
    def _validate_publication_after_recording(recording_end: datetime, publication_date: datetime) -> None:
        if publication_date <= recording_end:
            raise ValueError(
                "A data de publicação deve ser posterior ao término da gravação (após 23h50)."
            )
