"""
Pytest configuration and fixtures

Global fixtures for all tests.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_notion_response():
    """Mock successful Notion API response"""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "object": "page",
        "id": "test_page_id",
        "created_time": "2025-10-22T19:00:00.000Z",
        "last_edited_time": "2025-10-22T19:00:00.000Z",
        "properties": {},
    }
    return response


@pytest.fixture
def mock_error_response():
    """Mock error Notion API response"""
    response = MagicMock()
    response.status_code = 400
    response.text = "Bad Request"
    response.json.return_value = {
        "object": "error",
        "status": 400,
        "code": "validation_error",
        "message": "Invalid request",
    }
    return response

