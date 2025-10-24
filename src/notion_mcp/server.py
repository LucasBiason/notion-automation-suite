"""
MCP Server for Notion Integration

Implements Model Context Protocol server with custom Notion tools.
"""

import asyncio
import os
import sys
from typing import Any, Dict

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI

from notion_mcp.custom import PersonalNotion, StudyNotion, WorkNotion, YoutuberNotion
from notion_mcp.services.notion_service import NotionService
from notion_mcp.tools import (
    BaseNotionTools,
    PersonalNotionTools,
    StudyNotionTools,
    WorkNotionTools,
    YoutuberNotionTools,
)
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
                    message=f"No database ID configured for {db_type.value}",
                )

        # Initialize service
        self.service = NotionService(self.token)

        # Initialize custom implementations
        self.work_notion = (
            WorkNotion(self.service, self.database_ids[DatabaseType.WORK])
            if self.database_ids[DatabaseType.WORK]
            else None
        )

        self.study_notion = (
            StudyNotion(self.service, self.database_ids[DatabaseType.STUDIES])
            if self.database_ids[DatabaseType.STUDIES]
            else None
        )

        self.youtuber_notion = (
            YoutuberNotion(self.service, self.database_ids[DatabaseType.YOUTUBER])
            if self.database_ids[DatabaseType.YOUTUBER]
            else None
        )

        self.personal_notion = (
            PersonalNotion(self.service, self.database_ids[DatabaseType.PERSONAL])
            if self.database_ids[DatabaseType.PERSONAL]
            else None
        )

        # Initialize tool handlers
        self.base_tools = BaseNotionTools(self.service)
        self.work_tools = WorkNotionTools(self.work_notion) if self.work_notion else None
        self.study_tools = StudyNotionTools(self.study_notion) if self.study_notion else None
        self.youtuber_tools = (
            YoutuberNotionTools(self.youtuber_notion) if self.youtuber_notion else None
        )
        self.personal_tools = (
            PersonalNotionTools(self.personal_notion) if self.personal_notion else None
        )

        logger.info(
            "mcp_server_initialized",
            work_enabled=self.work_notion is not None,
            study_enabled=self.study_notion is not None,
            youtuber_enabled=self.youtuber_notion is not None,
            personal_enabled=self.personal_notion is not None,
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
        tools.extend(self.base_tools.get_tools())

        # WorkNotion tools
        if self.work_tools:
            tools.extend(self.work_tools.get_tools())

        # StudyNotion tools
        if self.study_tools:
            tools.extend(self.study_tools.get_tools())

        # YoutuberNotion tools
        if self.youtuber_tools:
            tools.extend(self.youtuber_tools.get_tools())

        # PersonalNotion tools
        if self.personal_tools:
            tools.extend(self.personal_tools.get_tools())

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

        # Check if it's a base tool
        if tool_name.startswith("notion_"):
            return await self.base_tools.handle_tool_call(tool_name, arguments)

        # Check if it's a work tool
        elif tool_name.startswith("work_") and self.work_tools:
            return await self.work_tools.handle_tool_call(tool_name, arguments)

        # Check if it's a study tool
        elif tool_name.startswith("study_") and self.study_tools:
            return await self.study_tools.handle_tool_call(tool_name, arguments)

        # Check if it's a youtuber tool
        elif tool_name.startswith("youtuber_") and self.youtuber_tools:
            return await self.youtuber_tools.handle_tool_call(tool_name, arguments)

        # Check if it's a personal tool
        elif tool_name.startswith("personal_") and self.personal_tools:
            return await self.personal_tools.handle_tool_call(tool_name, arguments)

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
                    "id": request.get("id") if "request" in locals() else None,
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
