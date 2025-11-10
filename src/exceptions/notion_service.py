"""Custom exceptions for Notion service operations."""

from __future__ import annotations


class NotionAPIError(Exception):
    """Base exception for Notion API errors."""


class NotionRateLimitError(NotionAPIError):
    """Raised when the Notion API signals a rate limit condition."""
