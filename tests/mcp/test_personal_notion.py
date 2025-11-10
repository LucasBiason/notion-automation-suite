"""Tests for PersonalNotion templates and helpers."""
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from notion_mcp.custom.personal_notion import PersonalNotion
from notion_mcp.services.notion_service import NotionService


@pytest.fixture
def personal_notion() -> PersonalNotion:
    service = NotionService(token="test_token")
    return PersonalNotion(service, database_id="personal_db")


@pytest.mark.asyncio
async def test_use_template_calls_create_card(personal_notion: PersonalNotion) -> None:
    reference = datetime(2025, 1, 6)
    with patch.object(personal_notion, "create_card", new=AsyncMock(return_value={"id": "task"})) as mock_create:
        await personal_notion.use_template("planejamento_semanal", reference)

    mock_create.assert_awaited_once()
    call_kwargs = mock_create.call_args.kwargs
    assert call_kwargs["title"] == PersonalNotion.TEMPLATES["planejamento_semanal"]["title"]
    assert "data" in call_kwargs


@pytest.mark.asyncio
async def test_create_weekly_cards_uses_all_templates(personal_notion: PersonalNotion) -> None:
    with patch.object(personal_notion, "use_template", new=AsyncMock(return_value={"id": "card"})) as mock_use:
        result = await personal_notion.create_weekly_cards(datetime(2025, 1, 6))

    assert set(result.keys()) == {"planejamento_semanal", "hamilton", "tratamento"}
    assert mock_use.await_count == 3


@pytest.mark.asyncio
async def test_create_monthly_events(personal_notion: PersonalNotion) -> None:
    with patch.object(personal_notion, "use_template", new=AsyncMock(return_value={"id": "event"})) as mock_use:
        result = await personal_notion.create_monthly_events(year=2025, month=1)

    assert set(result.keys()) == {"nf", "fechamento", "revisao_financeira"}
    assert mock_use.await_count == 3


@pytest.mark.asyncio
async def test_create_medical_appointment(personal_notion: PersonalNotion) -> None:
    appointment = {"id": "appointment"}
    with patch.object(personal_notion.service, "create_page", new=AsyncMock(return_value=appointment)) as mock_create:
        result = await personal_notion.create_medical_appointment(
            doctor="Silva",
            specialty="Cardiologia",
            date=datetime(2025, 1, 10, 15, 0),
            duration_minutes=90,
        )

    assert result == appointment
    props = mock_create.call_args.kwargs["properties"]
    assert props["Atividade"]["select"]["name"] == "Consulta Médica"
    date_payload = props["Data"]["date"]
    assert date_payload["start"].endswith("-03:00")
