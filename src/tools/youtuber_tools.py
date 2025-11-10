"""
Youtuber Notion MCP Tools

Provides specialized tools for youtuber database operations.
"""
from datetime import datetime
from typing import Any, Dict, List

import structlog

from utils.constants import YoutuberStatus

logger = structlog.get_logger(__name__)

STATUS_OPTIONS = [status.value for status in YoutuberStatus]


class YoutuberNotionTools:
    """Tools for youtuber database operations"""

    def __init__(self, youtuber_notion):
        self.youtuber_notion = youtuber_notion

    def _ensure_available(self) -> None:
        if self.youtuber_notion is None:
            raise ValueError(
                "Youtuber database is not configured for this MCP server. Configure NOTION_YOUTUBER_DATABASE_ID first."
            )

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return tool metadata for the youtuber database."""
        return [
            {
                "name": "youtuber_create_series",
                "description": "Create a full series with automatically scheduled episodes.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "sinopse": {"type": "string"},
                        "total_episodes": {"type": "integer", "minimum": 1},
                        "first_recording": {"type": "string", "description": "ISO 8601"},
                        "recording_interval_days": {"type": "integer", "default": 1},
                        "publication_hour": {"type": "integer", "default": 12},
                        "icon": {"type": "string"},
                        "episodes": {
                            "type": "array",
                            "description": "Override automatically generated episodes.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "recording_date": {"type": "string", "description": "ISO 8601"},
                                    "publication_date": {"type": "string", "description": "ISO 8601"},
                                    "status": {"type": "string", "enum": STATUS_OPTIONS},
                                    "resumo_episodio": {"type": "string"},
                                    "icon": {"type": "string"},
                                },
                            },
                        },
                    },
                    "required": ["title", "sinopse", "total_episodes", "first_recording"],
                },
            },
            {
                "name": "youtuber_create_episode",
                "description": "Create an episode linked to an existing series.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "episode_number": {"type": "integer", "minimum": 1},
                        "title": {"type": "string"},
                        "recording_date": {"type": "string", "description": "ISO 8601"},
                        "publication_date": {"type": "string", "description": "ISO 8601"},
                        "resumo_episodio": {"type": "string"},
                        "status": {"type": "string", "enum": STATUS_OPTIONS, "default": YoutuberStatus.PARA_GRAVAR.value},
                        "icon": {"type": "string", "default": "📺"},
                    },
                    "required": [
                        "parent_id",
                        "episode_number",
                        "title",
                        "recording_date",
                        "publication_date",
                    ],
                },
            },
            {
                "name": "youtuber_schedule_recordings",
                "description": "Generate sequential episodes for an existing series.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "series_id": {"type": "string"},
                        "total_episodes": {"type": "integer", "minimum": 1},
                        "start_recording": {"type": "string", "description": "ISO 8601"},
                        "recording_interval_days": {"type": "integer", "default": 1},
                        "publication_hour": {"type": "integer", "default": 12},
                        "base_title": {"type": "string", "default": "Episode"},
                    },
                    "required": ["series_id", "total_episodes", "start_recording"],
                },
            },
            {
                "name": "youtuber_update_episode_status",
                "description": "Update the status of an episode (Para Gravar, Gravado, Publicado).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {"type": "string"},
                        "status": {"type": "string", "enum": STATUS_OPTIONS},
                    },
                    "required": ["episode_id", "status"],
                },
            },
            {
                "name": "youtuber_reschedule_episode",
                "description": "Reschedule the recording and/or publication of an episode.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {"type": "string"},
                        "new_recording_date": {"type": "string", "description": "ISO 8601"},
                        "new_publication_date": {"type": "string", "description": "ISO 8601"},
                    },
                    "required": ["episode_id"],
                },
            },
            {
                "name": "youtuber_query_schedule",
                "description": "Query episodes filtered by status and release window.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": STATUS_OPTIONS},
                        "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                        "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 50},
                    },
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Dispatch youtuber tool calls."""
        logger.info("handling_youtuber_tool", tool=tool_name, args=arguments)
        self._ensure_available()

        if tool_name == "youtuber_create_series":
            episodes = arguments.pop("episodes", None) or []
            for episode in episodes:
                if "recording_date" in episode:
                    episode["recording_date"] = datetime.fromisoformat(episode["recording_date"])
                if "publication_date" in episode:
                    episode["publication_date"] = datetime.fromisoformat(episode["publication_date"])
            first_recording = datetime.fromisoformat(arguments.pop("first_recording"))
            return await self.youtuber_notion.create_series(
                first_recording=first_recording,
                episodes=episodes,
                **arguments,
            )

        if tool_name == "youtuber_create_episode":
            recording = datetime.fromisoformat(arguments.pop("recording_date"))
            publication = datetime.fromisoformat(arguments.pop("publication_date"))
            return await self.youtuber_notion.create_episode(
                recording_date=recording,
                publication_date=publication,
                **arguments,
            )

        if tool_name == "youtuber_schedule_recordings":
            start_recording = datetime.fromisoformat(arguments.pop("start_recording"))
            return await self.youtuber_notion.schedule_recordings(
                start_recording=start_recording,
                **arguments,
            )

        if tool_name == "youtuber_update_episode_status":
            return await self.youtuber_notion.update_episode_status(**arguments)

        if tool_name == "youtuber_reschedule_episode":
            new_recording = (
                datetime.fromisoformat(arguments.pop("new_recording_date"))
                if "new_recording_date" in arguments
                else None
            )
            new_publication = (
                datetime.fromisoformat(arguments.pop("new_publication_date"))
                if "new_publication_date" in arguments
                else None
            )
            return await self.youtuber_notion.reschedule_episode(
                new_recording_date=new_recording,
                new_publication_date=new_publication,
                **arguments,
            )

        if tool_name == "youtuber_query_schedule":
            return await self.youtuber_notion.query_schedule(**arguments)

        raise ValueError(f"Unknown youtuber tool: {tool_name}")
