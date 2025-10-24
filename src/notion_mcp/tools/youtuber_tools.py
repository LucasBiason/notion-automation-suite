"""
Youtuber Notion MCP Tools

Provides specialized tools for youtuber database operations.
"""

from typing import Any, Dict, List

import structlog

logger = structlog.get_logger(__name__)


class YoutuberNotionTools:
    """Tools for youtuber database operations"""

    def __init__(self, youtuber_notion):
        self.youtuber_notion = youtuber_notion

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get youtuber-specific tools"""
        return [
            {
                "name": "youtuber_create_series",
                "description": "Create YouTube series (recording period, NO publication date)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "first_recording": {"type": "string", "description": "ISO datetime"},
                        "last_recording": {"type": "string", "description": "ISO datetime"},
                        "icon": {"type": "string", "description": "Emoji icon"},
                    },
                    "required": ["title", "first_recording", "last_recording"],
                },
            },
            {
                "name": "youtuber_create_episode",
                "description": "Create episode (WITH publication date, episode 1 needs synopsis)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "parent_id": {"type": "string"},
                        "episode_number": {"type": "number"},
                        "title": {"type": "string"},
                        "recording_date": {"type": "string", "description": "ISO datetime"},
                        "publication_date": {"type": "string", "description": "ISO datetime"},
                        "resumo_episodio": {
                            "type": "string",
                            "description": "Required for episode 1",
                        },
                        "status": {"type": "string", "default": "Para gravar"},
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
                "description": "Schedule multiple episodes for a series",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "series_id": {"type": "string"},
                        "episode_count": {"type": "number"},
                        "start_recording": {"type": "string", "description": "ISO datetime"},
                        "recording_schedule": {
                            "type": "string",
                            "description": "daily, weekly, etc",
                        },
                        "publication_delay_hours": {"type": "number", "default": 15},
                    },
                    "required": ["series_id", "episode_count", "start_recording"],
                },
            },
            {
                "name": "youtuber_update_episode_status",
                "description": "Update episode status (Para gravar, Gravado, Publicado)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {"type": "string"},
                        "status": {"type": "string"},
                    },
                    "required": ["episode_id", "status"],
                },
            },
            {
                "name": "youtuber_reschedule_episode",
                "description": "Reschedule episode recording or publication",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "episode_id": {"type": "string"},
                        "new_recording_date": {"type": "string", "description": "ISO datetime"},
                        "new_publication_date": {"type": "string", "description": "ISO datetime"},
                    },
                    "required": ["episode_id"],
                },
            },
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Handle youtuber tool calls"""
        logger.info("handling_youtuber_tool", tool=tool_name, args=arguments)

        if tool_name == "youtuber_create_series":
            periodo = {
                "start": arguments.pop("first_recording"),
                "end": arguments.pop("last_recording"),
            }
            return await self.youtuber_notion.create_card(periodo=periodo, **arguments)

        elif tool_name == "youtuber_create_episode":
            from datetime import datetime

            recording = datetime.fromisoformat(arguments.pop("recording_date"))
            publication = datetime.fromisoformat(arguments.pop("publication_date"))
            return await self.youtuber_notion.create_episode(
                recording_date=recording, publication_date=publication, **arguments
            )

        elif tool_name == "youtuber_schedule_recordings":
            from datetime import datetime

            start = datetime.fromisoformat(arguments.pop("start_recording"))
            return await self.youtuber_notion.schedule_recordings(
                start_recording=start, **arguments
            )

        elif tool_name == "youtuber_update_episode_status":
            return await self.youtuber_notion.update_episode_status(**arguments)

        elif tool_name == "youtuber_reschedule_episode":
            from datetime import datetime

            new_recording = None
            new_publication = None

            if "new_recording_date" in arguments:
                new_recording = datetime.fromisoformat(arguments.pop("new_recording_date"))
            if "new_publication_date" in arguments:
                new_publication = datetime.fromisoformat(arguments.pop("new_publication_date"))

            return await self.youtuber_notion.reschedule_episode(
                new_recording_date=new_recording, new_publication_date=new_publication, **arguments
            )

        else:
            raise ValueError(f"Unknown youtuber tool: {tool_name}")
