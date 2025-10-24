"""Custom Notion classes with business rules"""

from notion_mcp.custom.base import CustomNotion
from notion_mcp.custom.personal_notion import PersonalNotion
from notion_mcp.custom.study_notion import StudyNotion
from notion_mcp.custom.work_notion import WorkNotion
from notion_mcp.custom.youtuber_notion import YoutuberNotion

__all__ = [
    "CustomNotion",
    "WorkNotion",
    "StudyNotion",
    "YoutuberNotion",
    "PersonalNotion",
]
