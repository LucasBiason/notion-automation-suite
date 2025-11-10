"""
Tests for WorkNotion

Tests for work-specific Notion implementation.
"""

from unittest.mock import AsyncMock, patch

import pytest

from notion_mcp.custom.work_notion import WorkNotion
from notion_mcp.services.notion_service import NotionService


@pytest.fixture
def work_notion():
    """Create WorkNotion instance for testing"""
    service = NotionService(token="test_token")
    return WorkNotion(service, database_id="test_work_db")


@pytest.mark.asyncio
async def test_create_project_with_defaults(work_notion):
    """Test project creation with default values"""
    mock_page = {"id": "test_project_id", "object": "page"}

    with patch.object(work_notion.service, "create_page", new=AsyncMock(return_value=mock_page)) as mock_create:
        await work_notion.create_card(title="Test Project")

    # Verify defaults
    call_args = mock_create.call_args
    properties = call_args.kwargs["properties"]

    assert properties["Cliente"]["select"]["name"] == "Astracode"
    assert properties["Prioridade"]["select"]["name"] == "Normal"
    assert properties["Status"]["status"]["name"] == "Não iniciado"

    # Verify icon
    assert call_args.kwargs["icon"]["type"] == "emoji"
    assert call_args.kwargs["icon"]["emoji"] == "🚀"


@pytest.mark.asyncio
async def test_create_project_custom_values(work_notion):
    """Test project creation with custom values"""
    mock_page = {"id": "test_id"}

    with patch.object(work_notion.service, "create_page", new=AsyncMock(return_value=mock_page)) as mock_create:
        await work_notion.create_card(
            title="Custom Project", cliente="FIAP", projeto="ExpenseIQ", prioridade="Alta", icon="🔐"
        )

    call_args = mock_create.call_args
    properties = call_args.kwargs["properties"]

    assert properties["Cliente"]["select"]["name"] == "FIAP"
    assert properties["Projeto"]["select"]["name"] == "ExpenseIQ"
    assert properties["Prioridade"]["select"]["name"] == "Alta"
    assert call_args.kwargs["icon"]["emoji"] == "🔐"


@pytest.mark.asyncio
async def test_create_subitem_with_relation(work_notion):
    """Test subitem creation with correct relation field"""
    mock_page = {"id": "test_subitem_id"}

    with patch.object(work_notion.service, "create_page", new=AsyncMock(return_value=mock_page)) as mock_create:
        await work_notion.create_subitem(parent_id="parent_xxx", title="My Subitem")

    call_args = mock_create.call_args
    properties = call_args.kwargs["properties"]

    # Verify relation field
    assert "Item Principal" in properties
    assert properties["Item Principal"]["relation"][0]["id"] == "parent_xxx"

    # Verify default icon for subitems
    assert call_args.kwargs["icon"]["emoji"] == "📋"


@pytest.mark.asyncio
async def test_update_status(work_notion):
    """Test status update"""
    mock_page = {"id": "test_id", "properties": {"Status": {"status": {"name": "Concluído"}}}}

    with patch.object(work_notion.service, "update_page", new=AsyncMock(return_value=mock_page)) as mock_update:
        await work_notion.update_status(page_id="test_id", status="Concluído")

    call_args = mock_update.call_args
    properties = call_args.kwargs["properties"]

    assert properties["Status"]["status"]["name"] == "Concluído"


@pytest.mark.asyncio
async def test_validation_emoji_in_title(work_notion):
    """Test that emojis in title raise validation error"""
    from notion_mcp.utils import ValidationError

    with pytest.raises(ValidationError, match="emojis"):
        await work_notion.create_card(title="🚀 My Project")
