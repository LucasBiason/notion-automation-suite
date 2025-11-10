"""Tests for MCP tool wrappers."""
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from notion_mcp.tools.personal_tools import PersonalNotionTools
from notion_mcp.tools.study_tools import StudyNotionTools
from notion_mcp.tools.work_tools import WorkNotionTools
from notion_mcp.tools.youtuber_tools import YoutuberNotionTools


@pytest.mark.asyncio
async def test_work_tool_create_sprint_calls_notional_method() -> None:
    notion = AsyncMock()
    tools = WorkNotionTools(notion)
    await tools.handle_tool_call(
        "work_create_sprint",
        {
            "title": "Sprint 1",
            "projeto": "ExpenseIQ",
            "cliente": "Astracode",
        },
    )
    notion.create_sprint.assert_awaited_once()


@pytest.mark.asyncio
async def test_study_tool_create_class_parses_datetime() -> None:
    notion = AsyncMock()
    tools = StudyNotionTools(notion)
    await tools.handle_tool_call(
        "study_create_class",
        {
            "parent_id": "section",
            "title": "Aula",
            "start_time": "2025-01-06T19:00:00",
            "duration_minutes": 90,
        },
    )
    notion.create_class.assert_awaited_once()
    args, kwargs = notion.create_class.call_args
    assert isinstance(kwargs["start_time"], datetime)


@pytest.mark.asyncio
async def test_personal_tool_use_template_converts_reference_date() -> None:
    notion = AsyncMock()
    tools = PersonalNotionTools(notion)
    await tools.handle_tool_call(
        "personal_use_template",
        {
            "template_name": "planejamento_semanal",
            "reference_date": "2025-01-06",
        },
    )
    notion.use_template.assert_awaited_once()
    _, kwargs = notion.use_template.call_args
    assert isinstance(kwargs["reference_date"], datetime)


@pytest.mark.asyncio
async def test_youtuber_tool_create_series_converts_dates() -> None:
    notion = AsyncMock()
    tools = YoutuberNotionTools(notion)
    await tools.handle_tool_call(
        "youtuber_create_series",
        {
            "title": "Série",
            "sinopse": "Sinopse",
            "total_episodes": 1,
            "first_recording": "2025-01-06T21:00:00",
        },
    )
    notion.create_series.assert_awaited_once()
    _, kwargs = notion.create_series.call_args
    assert isinstance(kwargs["first_recording"], datetime)
