"""
NotionService - Complete wrapper for Notion API

Provides all Notion API operations with error handling, retry logic,
and rate limiting.
"""

from typing import Any, Dict, List, Optional

import httpx
import structlog
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from exceptions import NotionAPIError, NotionRateLimitError
from utils.constants import NOTION_API_VERSION, NOTION_BASE_URL, REQUEST_TIMEOUT

logger = structlog.get_logger(__name__)

__all__ = ["NotionService", "NotionAPIError", "NotionRateLimitError"]


class NotionService:
    """
    Complete Notion API Service

    Provides all Notion API operations:
    - Pages (create, read, update, archive)
    - Databases (query, read)
    - Blocks (append, update, delete, read)
    - Users (list, read)
    - Search

    Features:
    - Automatic retry on transient errors
    - Rate limiting
    - Structured logging
    - Type validation
    """

    def __init__(self, token: str, version: str = NOTION_API_VERSION):
        """
        Initialize Notion service

        Args:
            token: Notion API token (integration token)
            version: Notion API version
        """
        self.token = token
        self.version = version
        self.base_url = NOTION_BASE_URL

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": version,
        }

        self.client = httpx.AsyncClient(
            headers=self.headers,
            timeout=REQUEST_TIMEOUT,
        )

        logger.info("notion_service_initialized", version=version)

    async def close(self) -> None:
        """Close HTTP client"""
        await self.client.aclose()

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Notion API with retry logic

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (without base URL)
            json_data: JSON body
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            NotionAPIError: On API error
            NotionRateLimitError: On rate limit exceeded
        """
        url = f"{self.base_url}/{endpoint}"

        logger.debug(
            "notion_api_request",
            method=method,
            endpoint=endpoint,
            has_body=json_data is not None,
        )

        try:
            response = await self._send_request(
                method=method,
                url=url,
                json_data=json_data,
                params=params,
            )
            return self._handle_response(endpoint, response)
        except httpx.TimeoutException as exc:
            logger.error("request_timeout", endpoint=endpoint, error=str(exc))
            raise
        except httpx.NetworkError as exc:
            logger.error("network_error", endpoint=endpoint, error=str(exc))
            raise

    async def _send_request(
        self,
        *,
        method: str,
        url: str,
        json_data: Optional[Dict[str, Any]],
        params: Optional[Dict[str, Any]],
    ) -> httpx.Response:
        return await self.client.request(
            method=method,
            url=url,
            json=json_data,
            params=params,
        )

    def _handle_response(self, endpoint: str, response: httpx.Response) -> Dict[str, Any]:
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            logger.warning("rate_limit_exceeded", retry_after=retry_after)
            raise NotionRateLimitError(
                f"Rate limit exceeded. Retry after {retry_after} seconds."
            )

        if response.status_code >= 400:
            error_data = response.json() if response.text else {}
            logger.error(
                "notion_api_error",
                status_code=response.status_code,
                error=error_data,
            )
            raise NotionAPIError(
                f"Notion API error {response.status_code}: "
                f"{error_data.get('message', response.text)}"
            )

        logger.debug("notion_api_success", endpoint=endpoint)
        return response.json()

    # ========== PAGES ==========

    async def create_page(
        self,
        database_id: str,
        properties: Dict[str, Any],
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
        children: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new page in a database

        Args:
            database_id: Target database ID
            properties: Page properties
            icon: Page icon (format: {"type": "emoji", "emoji": "🎓"})
            cover: Page cover image
            children: Initial page content blocks

        Returns:
            Created page object

        Example:
            >>> service = NotionService(token="secret_xxx")
            >>> page = await service.create_page(
            ...     database_id="xxx",
            ...     properties={
            ...         "Name": {"title": [{"text": {"content": "My Page"}}]}
            ...     },
            ...     icon={"type": "emoji", "emoji": "🎓"}
            ... )
        """
        payload: Dict[str, Any] = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }

        if icon:
            payload["icon"] = icon

        if cover:
            payload["cover"] = cover

        if children:
            payload["children"] = children

        logger.info("creating_page", database_id=database_id)

        return await self._request("POST", "pages", json_data=payload)

    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Retrieve a page by ID

        Args:
            page_id: Page ID

        Returns:
            Page object
        """
        logger.info("getting_page", page_id=page_id)
        return await self._request("GET", f"pages/{page_id}")

    async def update_page(
        self,
        page_id: str,
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
        archived: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Update a page

        Args:
            page_id: Page ID to update
            properties: Properties to update
            icon: New icon
            cover: New cover
            archived: Archive status

        Returns:
            Updated page object
        """
        payload: Dict[str, Any] = {}

        if properties is not None:
            payload["properties"] = properties

        if icon is not None:
            payload["icon"] = icon

        if cover is not None:
            payload["cover"] = cover

        if archived is not None:
            payload["archived"] = archived

        logger.info("updating_page", page_id=page_id)

        return await self._request("PATCH", f"pages/{page_id}", json_data=payload)

    async def archive_page(self, page_id: str) -> Dict[str, Any]:
        """
        Archive (soft delete) a page

        Args:
            page_id: Page ID to archive

        Returns:
            Archived page object
        """
        logger.info("archiving_page", page_id=page_id)
        return await self.update_page(page_id, archived=True)

    # ========== DATABASES ==========

    async def query_database(
        self,
        database_id: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, str]]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        """
        Query database with filters and sorting

        Args:
            database_id: Database ID to query
            filter_conditions: Filter conditions
            sorts: Sort configuration
            start_cursor: Pagination cursor
            page_size: Number of results per page (max 100)

        Returns:
            Query results with pagination info

        Example:
            >>> results = await service.query_database(
            ...     database_id="xxx",
            ...     filter_conditions={
            ...         "property": "Status",
            ...         "status": {"equals": "Concluído"}
            ...     }
            ... )
        """
        payload: Dict[str, Any] = {
            "page_size": min(page_size, 100),
        }

        if filter_conditions:
            payload["filter"] = filter_conditions

        if sorts:
            payload["sorts"] = sorts

        if start_cursor:
            payload["start_cursor"] = start_cursor

        logger.info("querying_database", database_id=database_id)

        return await self._request("POST", f"databases/{database_id}/query", json_data=payload)

    async def get_database(self, database_id: str) -> Dict[str, Any]:
        """
        Retrieve database schema

        Args:
            database_id: Database ID

        Returns:
            Database object with schema
        """
        logger.info("getting_database", database_id=database_id)
        return await self._request("GET", f"databases/{database_id}")

    # ========== BLOCKS ==========

    async def append_blocks(
        self,
        block_id: str,
        children: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Append blocks to a page or block

        Args:
            block_id: Parent block/page ID
            children: List of block objects

        Returns:
            Response with appended blocks

        Example:
            >>> blocks = [
            ...     {
            ...         "object": "block",
            ...         "type": "heading_1",
            ...         "heading_1": {
            ...             "rich_text": [{"type": "text", "text": {"content": "Title"}}]
            ...         }
            ...     }
            ... ]
            >>> await service.append_blocks(page_id, blocks)
        """
        payload = {"children": children}

        logger.info("appending_blocks", block_id=block_id, count=len(children))

        return await self._request("PATCH", f"blocks/{block_id}/children", json_data=payload)

    async def get_block(self, block_id: str) -> Dict[str, Any]:
        """
        Retrieve a block by ID

        Args:
            block_id: Block ID

        Returns:
            Block object
        """
        logger.info("getting_block", block_id=block_id)
        return await self._request("GET", f"blocks/{block_id}")

    async def get_block_children(
        self,
        block_id: str,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        """
        Retrieve children blocks of a block

        Args:
            block_id: Parent block ID
            start_cursor: Pagination cursor
            page_size: Results per page

        Returns:
            List of child blocks
        """
        params = {"page_size": min(page_size, 100)}

        if start_cursor:
            params["start_cursor"] = start_cursor

        logger.info("getting_block_children", block_id=block_id)

        return await self._request("GET", f"blocks/{block_id}/children", params=params)

    async def update_block(
        self,
        block_id: str,
        block_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update a block

        Args:
            block_id: Block ID to update
            block_data: New block data

        Returns:
            Updated block object
        """
        logger.info("updating_block", block_id=block_id)
        return await self._request("PATCH", f"blocks/{block_id}", json_data=block_data)

    async def delete_block(self, block_id: str) -> Dict[str, Any]:
        """
        Delete a block

        Args:
            block_id: Block ID to delete

        Returns:
            Deleted block object
        """
        logger.info("deleting_block", block_id=block_id)
        return await self._request("DELETE", f"blocks/{block_id}")

    # ========== USERS ==========

    async def list_users(
        self,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        """
        List all users in workspace

        Args:
            start_cursor: Pagination cursor
            page_size: Results per page

        Returns:
            List of users
        """
        params = {"page_size": min(page_size, 100)}

        if start_cursor:
            params["start_cursor"] = start_cursor

        logger.info("listing_users")
        return await self._request("GET", "users", params=params)

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve a user by ID

        Args:
            user_id: User ID

        Returns:
            User object
        """
        logger.info("getting_user", user_id=user_id)
        return await self._request("GET", f"users/{user_id}")

    async def get_me(self) -> Dict[str, Any]:
        """
        Retrieve bot user info

        Returns:
            Bot user object
        """
        logger.info("getting_bot_user")
        return await self._request("GET", "users/me")

    # ========== SEARCH ==========

    async def search(
        self,
        query: Optional[str] = None,
        filter_conditions: Optional[Dict[str, Any]] = None,
        sort: Optional[Dict[str, str]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        """
        Search pages and databases

        Args:
            query: Search query string
            filter_conditions: Filter configuration
            sort: Sort configuration
            start_cursor: Pagination cursor
            page_size: Results per page

        Returns:
            Search results

        Example:
            >>> results = await service.search(
            ...     query="Project",
            ...     filter_conditions={"property": "object", "value": "page"}
            ... )
        """
        payload: Dict[str, Any] = {
            "page_size": min(page_size, 100),
        }

        if query:
            payload["query"] = query

        if filter_conditions:
            payload["filter"] = filter_conditions

        if sort:
            payload["sort"] = sort

        if start_cursor:
            payload["start_cursor"] = start_cursor

        logger.info("searching", query=query)

        return await self._request("POST", "search", json_data=payload)

    # ========== HELPER METHODS ==========

    def build_rich_text(self, content: str) -> List[Dict[str, Any]]:
        """
        Build rich text array for Notion

        Args:
            content: Text content

        Returns:
            Rich text array
        """
        return [{"type": "text", "text": {"content": content}}]

    def build_title_property(self, title: str) -> Dict[str, Any]:
        """
        Build title property

        Args:
            title: Title text

        Returns:
            Title property dict
        """
        return {"title": self.build_rich_text(title)}

    def build_rich_text_property(self, text: str) -> Dict[str, Any]:
        """
        Build rich text property

        Args:
            text: Text content

        Returns:
            Rich text property dict
        """
        return {"rich_text": self.build_rich_text(text)}

    def build_select_property(self, value: str) -> Dict[str, Any]:
        """
        Build select property

        Args:
            value: Select option value

        Returns:
            Select property dict
        """
        return {"select": {"name": value}}

    def build_multi_select_property(self, values: List[str]) -> Dict[str, Any]:
        """
        Build multi-select property

        Args:
            values: List of option values

        Returns:
            Multi-select property dict
        """
        return {"multi_select": [{"name": v} for v in values]}

    def build_status_property(self, status: str) -> Dict[str, Any]:
        """
        Build status property

        Args:
            status: Status value

        Returns:
            Status property dict
        """
        return {"status": {"name": status}}

    def build_date_property(
        self,
        start: str,
        end: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build date property

        Args:
            start: Start date/datetime (ISO format)
            end: End date/datetime (ISO format, optional)

        Returns:
            Date property dict
        """
        date_dict = {"start": start}

        if end:
            date_dict["end"] = end

        return {"date": date_dict}

    def build_relation_property(self, page_ids: List[str]) -> Dict[str, Any]:
        """
        Build relation property

        Args:
            page_ids: List of related page IDs

        Returns:
            Relation property dict
        """
        return {"relation": [{"id": pid} for pid in page_ids]}

    def build_number_property(self, number: float) -> Dict[str, Any]:
        """
        Build number property

        Args:
            number: Number value

        Returns:
            Number property dict
        """
        return {"number": number}

    def build_checkbox_property(self, checked: bool) -> Dict[str, Any]:
        """
        Build checkbox property

        Args:
            checked: Checkbox state

        Returns:
            Checkbox property dict
        """
        return {"checkbox": checked}

    def build_url_property(self, url: str) -> Dict[str, Any]:
        """
        Build URL property

        Args:
            url: URL string

        Returns:
            URL property dict
        """
        return {"url": url}

    def build_email_property(self, email: str) -> Dict[str, Any]:
        """
        Build email property

        Args:
            email: Email string

        Returns:
            Email property dict
        """
        return {"email": email}

    def build_phone_property(self, phone: str) -> Dict[str, Any]:
        """
        Build phone property

        Args:
            phone: Phone string

        Returns:
            Phone property dict
        """
        return {"phone_number": phone}
