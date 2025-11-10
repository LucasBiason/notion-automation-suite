"""Exception types exposed by the Notion MCP package."""

from .notion_service import NotionAPIError, NotionRateLimitError

__all__ = ["NotionAPIError", "NotionRateLimitError"]
