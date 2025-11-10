"""Tests for YoutuberNotion operations."""
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from notion_mcp.custom.youtuber_notion import YoutuberNotion
from notion_mcp.services.notion_service import NotionService


@pytest.fixture
def youtuber_notion() -> YoutuberNotion:
    service = NotionService(token="test_token")
    return YoutuberNotion(service, database_id="youtuber_db")


@pytest.mark.asyncio
async def test_create_series_generates_episodes(youtuber_notion: YoutuberNotion) -> None:
    with (
        patch.object(youtuber_notion, "create_card", new=AsyncMock(return_value={"id": "series"})) as mock_series,
        patch.object(youtuber_notion, "create_episode", new=AsyncMock(return_value={"id": "episode"})) as mock_episode,
    ):
        result = await youtuber_notion.create_series(
            title="Nova Série",
            sinopse="Sinopse",
            total_episodes=2,
            first_recording=datetime(2025, 1, 6, 21, 0),
        )

    assert result["series"] == {"id": "series"}
    assert mock_series.await_count == 1
    assert mock_episode.await_count == 2


@pytest.mark.asyncio
async def test_schedule_recordings_creates_multiple_episodes(youtuber_notion: YoutuberNotion) -> None:
    with patch.object(youtuber_notion, "create_episode", new=AsyncMock(return_value={"id": "ep"})) as mock_episode:
        schedule = await youtuber_notion.schedule_recordings(
            series_id="series",
            total_episodes=3,
            start_recording=datetime(2025, 1, 6, 21, 0),
            recording_interval_days=2,
            publication_hour=10,
        )

    assert schedule["count"] == 3
    assert mock_episode.await_count == 3


@pytest.mark.asyncio
async def test_update_episode_status_calls_service(youtuber_notion: YoutuberNotion) -> None:
    with patch.object(youtuber_notion.service, "update_page", new=AsyncMock(return_value={"id": "ep"})) as mock_update:
        await youtuber_notion.update_episode_status("ep", "Gravando")

    properties = mock_update.call_args.kwargs["properties"]
    assert properties["Status"]["status"]["name"] == "Gravando"


@pytest.mark.asyncio
async def test_reschedule_episode_updates_dates(youtuber_notion: YoutuberNotion) -> None:
    new_recording = datetime(2025, 1, 8, 21, 0)
    new_publication = datetime(2025, 1, 9, 12, 0)
    with patch.object(youtuber_notion.service, "update_page", new=AsyncMock(return_value={"id": "ep"})) as mock_update:
        await youtuber_notion.reschedule_episode(
            episode_id="ep",
            new_recording_date=new_recording,
            new_publication_date=new_publication,
        )

    properties = mock_update.call_args.kwargs["properties"]
    assert properties["Data de Lançamento"]["date"]["start"].endswith("-03:00")
    assert properties["Periodo"]["date"]["start"].endswith("-03:00")


@pytest.mark.asyncio
async def test_query_schedule_passes_filters(youtuber_notion: YoutuberNotion) -> None:
    response = {"results": [], "has_more": False, "next_cursor": None}
    with patch.object(youtuber_notion.service, "query_database", new=AsyncMock(return_value=response)) as mock_query:
        await youtuber_notion.query_schedule(status="Para Gravar", start_date="2025-01-01", end_date="2025-01-31", limit=5)

    call_kwargs = mock_query.call_args.kwargs
    assert call_kwargs["page_size"] == 5
    filters = call_kwargs["filter_conditions"]["and"]
    assert any(filt["property"] == "Status" for filt in filters)
    assert any(filt["property"] == "Data de Lançamento" for filt in filters)
