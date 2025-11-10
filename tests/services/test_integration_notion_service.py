"""Integration-style tests for NotionService using httpx.MockTransport."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

import httpx
import pytest

from notion_mcp.services.notion_service import (
    NotionRateLimitError,
    NotionService,
)


class TransportRecorder:
    """Helper transport to capture the last outbound request."""

    def __init__(
        self,
        response_json: Dict[str, Any],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.response_json = response_json
        self.status_code = status_code
        self.headers = headers or {}
        self.last_request: Optional[httpx.Request] = None

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.last_request = request
        content = json.dumps(self.response_json).encode("utf-8")
        return httpx.Response(status_code=self.status_code, content=content, headers=self.headers)


async def _swap_transport(service: NotionService, transport: httpx.BaseTransport) -> None:
    await service.client.aclose()
    service.client = httpx.AsyncClient(transport=transport, headers=service.headers)


@pytest.mark.asyncio
async def test_create_page_payload_and_response() -> None:
    recorder = TransportRecorder({"id": "page_123", "object": "page"})
    transport = httpx.MockTransport(recorder.handler)

    service = NotionService(token="secret-token")
    await _swap_transport(service, transport)

    try:
        result = await service.create_page(
            database_id="db123",
            properties={"Name": {"title": [{"text": {"content": "Example"}}]}},
        )
    finally:
        await service.close()

    assert result["id"] == "page_123"
    assert recorder.last_request is not None
    request_json = json.loads(recorder.last_request.content.decode("utf-8"))
    assert request_json["parent"] == {"database_id": "db123"}
    assert request_json["properties"]["Name"]["title"][0]["text"]["content"] == "Example"
    assert "icon" not in request_json


@pytest.mark.asyncio
async def test_query_database_with_filters() -> None:
    recorder = TransportRecorder(
        {"results": [{"id": "page_a"}], "has_more": False, "next_cursor": None}
    )
    transport = httpx.MockTransport(recorder.handler)

    service = NotionService(token="secret-token")
    await _swap_transport(service, transport)

    try:
        response = await service.query_database(
            database_id="db123",
            filter_conditions={"property": "Status", "status": {"equals": "Em Progresso"}},
            sorts=[{"property": "Project name", "direction": "ascending"}],
            page_size=10,
        )
    finally:
        await service.close()

    assert response["results"][0]["id"] == "page_a"
    assert recorder.last_request is not None
    payload = json.loads(recorder.last_request.content.decode("utf-8"))
    assert payload["filter"]["status"]["equals"] == "Em Progresso"
    assert payload["sorts"][0]["property"] == "Project name"
    assert payload["page_size"] == 10


@pytest.mark.asyncio
async def test_rate_limit_raises_notation_error() -> None:
    recorder = TransportRecorder({}, status_code=429, headers={"Retry-After": "120"})
    transport = httpx.MockTransport(recorder.handler)

    service = NotionService(token="secret-token")
    await _swap_transport(service, transport)

    try:
        with pytest.raises(NotionRateLimitError):
            await service.create_page(database_id="db123", properties={"Name": {"title": []}})
    finally:
        await service.close()
