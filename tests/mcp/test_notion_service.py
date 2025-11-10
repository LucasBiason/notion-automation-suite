"""
Tests for NotionService

Basic tests for Notion API wrapper.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from notion_mcp.services.notion_service import NotionAPIError, NotionService


@pytest.fixture
def notion_service():
    """Create NotionService instance for testing"""
    return NotionService(token="test_token")


@pytest.mark.asyncio
async def test_create_page_success(notion_service):
    """Test successful page creation"""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "object": "page",
        "id": "test_page_id",
    }

    with patch.object(notion_service.client, "request", new=AsyncMock(return_value=mock_response)):
        result = await notion_service.create_page(
            database_id="test_db",
            properties={"Name": {"title": [{"text": {"content": "Test Page"}}]}},
        )

    assert result["id"] == "test_page_id"
    assert result["object"] == "page"


@pytest.mark.asyncio
async def test_create_page_with_icon(notion_service):
    """Test page creation with icon"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "test_id"}

    with patch.object(notion_service.client, "request", new=AsyncMock(return_value=mock_response)):
        result = await notion_service.create_page(
            database_id="test_db",
            properties={"Name": {"title": [{"text": {"content": "Test"}}]}},
            icon={"type": "emoji", "emoji": "🎓"},
        )

    assert result["id"] == "test_id"


@pytest.mark.asyncio
async def test_api_error_handling(notion_service):
    """Test API error handling"""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_response.json.return_value = {"message": "Invalid request"}

    with patch.object(notion_service.client, "request", new=AsyncMock(return_value=mock_response)), \
         pytest.raises(NotionAPIError):
        await notion_service.create_page(database_id="test_db", properties={})


@pytest.mark.asyncio
async def test_build_helpers(notion_service):
    """Test property builder helpers"""
    # Title
    title_prop = notion_service.build_title_property("My Title")
    assert title_prop["title"][0]["text"]["content"] == "My Title"

    # Rich text
    text_prop = notion_service.build_rich_text_property("Description")
    assert text_prop["rich_text"][0]["text"]["content"] == "Description"

    # Select
    select_prop = notion_service.build_select_property("Option 1")
    assert select_prop["select"]["name"] == "Option 1"

    # Status
    status_prop = notion_service.build_status_property("Concluído")
    assert status_prop["status"]["name"] == "Concluído"

    # Date
    date_prop = notion_service.build_date_property("2025-10-22", "2025-10-25")
    assert date_prop["date"]["start"] == "2025-10-22"
    assert date_prop["date"]["end"] == "2025-10-25"

    # Relation
    relation_prop = notion_service.build_relation_property(["id1", "id2"])
    assert len(relation_prop["relation"]) == 2
    assert relation_prop["relation"][0]["id"] == "id1"
