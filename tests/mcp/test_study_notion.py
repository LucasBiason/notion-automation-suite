"""Tests for StudyNotion functionality."""
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from notion_mcp.custom.study_notion import StudyNotion
from notion_mcp.services.notion_service import NotionService


@pytest.fixture
def study_notion() -> StudyNotion:
    service = NotionService(token="test_token")
    return StudyNotion(service, database_id="study_db")


@pytest.mark.asyncio
async def test_create_class_valid_schedule(study_notion: StudyNotion) -> None:
    mock_response = {"id": "class_001"}
    with patch.object(study_notion.service, "create_page", new=AsyncMock(return_value=mock_response)) as mock_create:
        await study_notion.create_class(
            parent_id="section_123",
            title="Aula 01",
            start_time=datetime(2025, 1, 6, 19, 0),
            duration_minutes=90,
        )

    properties = mock_create.call_args.kwargs["properties"]
    periodo = properties["Período"]["date"]
    assert periodo["start"].endswith("-03:00")
    assert periodo["end"].endswith("-03:00")
    assert properties["Status"]["status"]["name"] == "Para Fazer"


@pytest.mark.asyncio
async def test_create_class_invalid_schedule_raises(study_notion: StudyNotion) -> None:
    with pytest.raises(ValueError):
        await study_notion.create_class(
            parent_id="section_123",
            title="Aula 01",
            start_time=datetime(2025, 1, 6, 18, 0),
            duration_minutes=90,
        )


@pytest.mark.asyncio
async def test_create_course_complete_invokes_children(study_notion: StudyNotion) -> None:
    fases = [
        {
            "title": "Fase 1",
            "sections": [
                {
                    "title": "Seção 1",
                    "classes": [
                        {
                            "title": "Aula 01",
                            "start": "2025-01-06T19:00:00",
                            "duration_minutes": 90,
                        }
                    ],
                }
            ],
        }
    ]

    with (
        patch.object(study_notion, "create_card", new=AsyncMock(return_value={"id": "course"})) as mock_course,
        patch.object(study_notion, "create_phase", new=AsyncMock(return_value={"id": "phase"})) as mock_phase,
        patch.object(study_notion, "create_section", new=AsyncMock(return_value={"id": "section"})) as mock_section,
        patch.object(study_notion, "create_class", new=AsyncMock(return_value={"id": "class"})) as mock_class,
    ):
        result = await study_notion.create_course_complete(title="Curso", fases=fases)

    assert result["course"] == {"id": "course"}
    assert mock_course.await_count == 1
    assert mock_phase.await_count == 1
    assert mock_section.await_count == 1
    assert mock_class.await_count == 1


@pytest.mark.asyncio
async def test_query_schedule_builds_filters(study_notion: StudyNotion) -> None:
    response = {"results": [], "has_more": False, "next_cursor": None}
    with patch.object(study_notion.service, "query_database", new=AsyncMock(return_value=response)) as mock_query:
        await study_notion.query_schedule(status="Para Fazer", start_date="2025-01-01", end_date="2025-01-31", limit=10)

    call_kwargs = mock_query.call_args.kwargs
    assert call_kwargs["page_size"] == 10
    filters = call_kwargs["filter_conditions"]["and"]
    assert any(filt["property"] == "Status" for filt in filters)
    assert any(filt["property"] == "Período" for filt in filters)
