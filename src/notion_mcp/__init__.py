"""
Notion MCP Server

Complete MCP server for Notion integration with custom business rules
for multiple database types (Work, Studies, Personal, Youtuber).
"""

__version__ = "0.1.0"
__author__ = "Lucas Biason"
__email__ = "lucas.biason@gmail.com"

from notion_mcp.services.notion_service import NotionService
from notion_mcp.custom.work_notion import WorkNotion
from notion_mcp.custom.study_notion import StudyNotion
from notion_mcp.custom.youtuber_notion import YoutuberNotion
from notion_mcp.custom.personal_notion import PersonalNotion

__all__ = [
    "NotionService",
    "WorkNotion",
    "StudyNotion",
    "YoutuberNotion",
    "PersonalNotion",
]

