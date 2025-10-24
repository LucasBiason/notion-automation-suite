"""
MCP Server for Notion Integration

Implements Model Context Protocol server with custom Notion tools.
"""

import os
import sys
import asyncio
from typing import Any, Dict
import structlog
from fastapi import FastAPI
from dotenv import load_dotenv

from notion_mcp.services.notion_service import NotionService
from notion_mcp.custom import WorkNotion, StudyNotion, YoutuberNotion, PersonalNotion
from notion_mcp.utils import DatabaseType


# Load environment variables
load_dotenv()

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger(__name__)


class NotionMCPServer:
    """
    MCP Server for Notion Integration
    
    Provides tools for AI agents to interact with Notion using
    custom business rules for different database types.
    """
    
    def __init__(self):
        """Initialize MCP server"""
        # Load configuration
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable is required")
        
        self.database_ids = {
            DatabaseType.WORK: os.getenv("NOTION_WORK_DATABASE_ID"),
            DatabaseType.STUDIES: os.getenv("NOTION_STUDIES_DATABASE_ID"),
            DatabaseType.PERSONAL: os.getenv("NOTION_PERSONAL_DATABASE_ID"),
            DatabaseType.YOUTUBER: os.getenv("NOTION_YOUTUBER_DATABASE_ID"),
        }
        
        # Validate database IDs
        for db_type, db_id in self.database_ids.items():
            if not db_id:
                logger.warning(
                    "database_id_missing",
                    database_type=db_type.value,
                    message=f"No database ID configured for {db_type.value}"
                )
        
        # Initialize service
        self.service = NotionService(self.token)
        
        # Initialize custom implementations
        self.work = WorkNotion(self.service, self.database_ids[DatabaseType.WORK]) \
            if self.database_ids[DatabaseType.WORK] else None
        
        self.study = StudyNotion(self.service, self.database_ids[DatabaseType.STUDIES]) \
            if self.database_ids[DatabaseType.STUDIES] else None
        
        self.youtuber = YoutuberNotion(self.service, self.database_ids[DatabaseType.YOUTUBER]) \
            if self.database_ids[DatabaseType.YOUTUBER] else None
        
        self.personal = PersonalNotion(self.service, self.database_ids[DatabaseType.PERSONAL]) \
            if self.database_ids[DatabaseType.PERSONAL] else None
        
        logger.info(
            "mcp_server_initialized",
            work_enabled=self.work is not None,
            study_enabled=self.study is not None,
            youtuber_enabled=self.youtuber is not None,
            personal_enabled=self.personal is not None,
        )
    
    async def close(self) -> None:
        """Close server and cleanup resources"""
        await self.service.close()
        logger.info("mcp_server_closed")
    
    def get_tools(self) -> list:
        """
        Get all available MCP tools
        
        Returns:
            List of tool definitions for MCP protocol
        """
        tools = []
        
        # Base NotionService tools
        tools.extend([
            {
                "name": "notion_create_page",
                "description": "Create a page in Notion database (low-level API)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "database_id": {"type": "string"},
                        "properties": {"type": "object"},
                        "icon": {"type": "object"},
                    },
                    "required": ["database_id", "properties"],
                },
            },
            {
                "name": "notion_update_page",
                "description": "Update a Notion page (low-level API)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                        "properties": {"type": "object"},
                        "icon": {"type": "object"},
                    },
                    "required": ["page_id"],
                },
            },
            {
                "name": "notion_get_page",
                "description": "Get a Notion page by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string"},
                    },
                    "required": ["page_id"],
                },
            },
            {
                "name": "notion_query_database",
                "description": "Query Notion database with filters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "database_id": {"type": "string"},
                        "filter": {"type": "object"},
                        "sorts": {"type": "array"},
                    },
                    "required": ["database_id"],
                },
            },
        ])
        
        # WorkNotion tools
        if self.work:
            tools.extend([
                {
                    "name": "work_create_project",
                    "description": "Create work project with correct structure (client, project, priority)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Project title (without emojis)"},
                            "cliente": {"type": "string", "default": "Astracode"},
                            "projeto": {"type": "string", "description": "ExpenseIQ, HubTravel, etc"},
                            "prioridade": {"type": "string", "default": "Normal"},
                            "icon": {"type": "string", "description": "Emoji icon (e.g., 🚀)"},
                        },
                        "required": ["title"],
                    },
                },
                {
                    "name": "work_create_subitem",
                    "description": "Create work subitem linked to parent project",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "parent_id": {"type": "string"},
                            "title": {"type": "string"},
                            "prioridade": {"type": "string", "default": "Normal"},
                        },
                        "required": ["parent_id", "title"],
                    },
                },
            ])
        
        # StudyNotion tools
        if self.study:
            tools.extend([
                {
                    "name": "study_create_course",
                    "description": "Create study course (without time, only dates)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "categorias": {"type": "array", "items": {"type": "string"}},
                            "periodo_start": {"type": "string", "description": "YYYY-MM-DD"},
                            "periodo_end": {"type": "string", "description": "YYYY-MM-DD"},
                        },
                        "required": ["title"],
                    },
                },
                {
                    "name": "study_create_class",
                    "description": "Create study class with correct hours (19:00-21:00, Tuesday 19:30)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "parent_id": {"type": "string"},
                            "title": {"type": "string"},
                            "start_time": {"type": "string", "description": "ISO datetime"},
                            "duration_minutes": {"type": "number"},
                        },
                        "required": ["parent_id", "title", "start_time", "duration_minutes"],
                    },
                },
            ])
        
        # YoutuberNotion tools
        if self.youtuber:
            tools.extend([
                {
                    "name": "youtuber_create_series",
                    "description": "Create YouTube series (recording period, NO publication date)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "first_recording": {"type": "string", "description": "ISO datetime"},
                            "last_recording": {"type": "string", "description": "ISO datetime"},
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
                            "recording_date": {"type": "string"},
                            "publication_date": {"type": "string"},
                            "resumo_episodio": {"type": "string", "description": "Required for episode 1"},
                        },
                        "required": ["parent_id", "episode_number", "title", "recording_date", "publication_date"],
                    },
                },
            ])
        
        # PersonalNotion tools
        if self.personal:
            tools.extend([
                {
                    "name": "personal_create_task",
                    "description": "Create personal task/event (uses 'Data' field, not 'Período')",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "atividade": {"type": "string"},
                            "data_start": {"type": "string"},
                            "data_end": {"type": "string"},
                        },
                        "required": ["title"],
                    },
                },
                {
                    "name": "personal_create_subtask",
                    "description": "Create personal subtask linked to parent",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "parent_id": {"type": "string"},
                            "title": {"type": "string"},
                        },
                        "required": ["parent_id", "title"],
                    },
                },
            ])
        
        return tools
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Handle MCP tool call
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
        
        Returns:
            Tool execution result
        """
        logger.info("handling_tool_call", tool=tool_name, args=arguments)
        
        # Base NotionService tools
        if tool_name == "notion_create_page":
            return await self.service.create_page(**arguments)
        
        elif tool_name == "notion_update_page":
            return await self.service.update_page(**arguments)
        
        elif tool_name == "notion_get_page":
            return await self.service.get_page(**arguments)
        
        elif tool_name == "notion_query_database":
            return await self.service.query_database(**arguments)
        
        # WorkNotion tools
        elif tool_name == "work_create_project" and self.work:
            return await self.work.create_card(**arguments)
        
        elif tool_name == "work_create_subitem" and self.work:
            return await self.work.create_subitem(**arguments)
        
        # StudyNotion tools
        elif tool_name == "study_create_course" and self.study:
            periodo = None
            if 'periodo_start' in arguments:
                periodo = {'start': arguments.pop('periodo_start')}
                if 'periodo_end' in arguments:
                    periodo['end'] = arguments.pop('periodo_end')
            return await self.study.create_card(periodo=periodo, **arguments)
        
        elif tool_name == "study_create_class" and self.study:
            from datetime import datetime
            start = datetime.fromisoformat(arguments.pop('start_time'))
            return await self.study.create_class(start_time=start, **arguments)
        
        # YoutuberNotion tools
        elif tool_name == "youtuber_create_series" and self.youtuber:
            periodo = {
                'start': arguments.pop('first_recording'),
                'end': arguments.pop('last_recording'),
            }
            return await self.youtuber.create_card(periodo=periodo, **arguments)
        
        elif tool_name == "youtuber_create_episode" and self.youtuber:
            from datetime import datetime
            recording = datetime.fromisoformat(arguments.pop('recording_date'))
            publication = datetime.fromisoformat(arguments.pop('publication_date'))
            return await self.youtuber.create_episode(
                recording_date=recording,
                publication_date=publication,
                **arguments
            )
        
        # PersonalNotion tools
        elif tool_name == "personal_create_task" and self.personal:
            data = None
            if 'data_start' in arguments:
                data = {'start': arguments.pop('data_start')}
                if 'data_end' in arguments:
                    data['end'] = arguments.pop('data_end')
            return await self.personal.create_card(data=data, **arguments)
        
        elif tool_name == "personal_create_subtask" and self.personal:
            return await self.personal.create_subitem(**arguments)
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")


# FastAPI app for HTTP interface (optional)
app = FastAPI(
    title="Notion MCP Server",
    description="Complete MCP server for Notion integration",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "notion-mcp-server", "version": "0.1.0"}


@app.get("/tools")
async def list_tools():
    """List available tools"""
    server = NotionMCPServer()
    tools = server.get_tools()
    await server.close()
    return {"tools": tools, "count": len(tools)}


def main():
    """
    Main entry point for MCP server
    
    This implements the MCP stdio protocol for use with AI assistants.
    """
    import json
    
    logger.info("starting_mcp_server")
    
    try:
        server = NotionMCPServer()
        
        # MCP stdio protocol implementation
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            
            try:
                request = json.loads(line)
                
                # Handle different MCP requests
                if request.get("method") == "tools/list":
                    tools = server.get_tools()
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {"tools": tools},
                    }
                
                elif request.get("method") == "tools/call":
                    params = request.get("params", {})
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    
                    result = asyncio.run(server.handle_tool_call(tool_name, arguments))
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                    }
                
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {
                            "code": -32601,
                            "message": f"Unknown method: {request.get('method')}",
                        },
                    }
                
                print(json.dumps(response), flush=True)
            
            except Exception as e:
                logger.error("request_error", error=str(e))
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e),
                    },
                }
                print(json.dumps(error_response), flush=True)
    
    except KeyboardInterrupt:
        logger.info("server_interrupted")
    
    finally:
        asyncio.run(server.close())
        logger.info("server_shutdown")


if __name__ == "__main__":
    main()

