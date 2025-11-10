"""STDIO loop implementation for the Notion MCP server."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any, Dict, Optional

import structlog

from .notion_server import NotionMCPServer

logger = structlog.get_logger(__name__)


class MCPStdIOServer:
    """JSON-RPC server that speaks MCP over standard IO."""

    def __init__(self, notion_server: NotionMCPServer) -> None:
        self._notion_server = notion_server

    async def run(self) -> None:
        loop = asyncio.get_running_loop()
        logger.info("mcp_stdio_server_started")
        try:
            while True:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if line == "":
                    break
                stripped = line.strip()
                if not stripped:
                    continue
                response = await self._handle_line(stripped)
                if response is not None:
                    await self._write_response(response)
        except KeyboardInterrupt:
            logger.info("mcp_stdio_interrupted")
        finally:
            await self._notion_server.close()
            logger.info("mcp_stdio_server_stopped")

    async def _handle_line(self, raw_line: str) -> Optional[Dict[str, Any]]:
        try:
            request = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            logger.error("invalid_json", error=str(exc))
            return self._build_error_response(None, -32700, f"Invalid JSON: {exc.msg}")
        try:
            return await self._handle_request(request)
        except Exception as exc:  # pragma: no cover - defensive response path
            logger.error("request_processing_error", error=str(exc))
            return self._build_error_response(request.get("id"), -32603, str(exc))

    async def _handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        request_id = request.get("id")

        if method == "initialize":
            return self._build_success_response(
                request_id,
                {
                    "capabilities": {
                        "tools": {"list": True, "call": True},
                        "resources": {"list": True, "read": True},
                        "prompts": {"list": True},
                    }
                },
            )

        if method == "tools/list":
            tools = self._notion_server.get_tools()
            return self._build_success_response(request_id, {"tools": tools})

        if method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {}) if params else {}
            if not tool_name:
                raise ValueError("Tool name is required for tools/call")
            result = await self._notion_server.handle_tool_call(tool_name, arguments)
            content = [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]
            return self._build_success_response(request_id, {"content": content})

        if method == "resources/list":
            resources = self._notion_server.get_resources()
            return self._build_success_response(request_id, {"resources": resources})

        if method == "resources/read":
            params = request.get("params", {})
            uri = params.get("uri") if params else None
            resource_content = await self._notion_server.read_resource(uri)
            return self._build_success_response(request_id, {"contents": [resource_content]})

        if method == "prompts/list":
            return self._build_success_response(request_id, {"prompts": self._notion_server.get_prompts()})

        if method == "notifications/subscribe":
            return self._build_success_response(request_id, {})

        if method == "ping":
            return self._build_success_response(request_id, {"pong": True})

        raise ValueError(f"Unknown method: {method}")

    @staticmethod
    def _build_success_response(request_id: Any, result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        response: Dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
        response["result"] = result or {}
        return response

    @staticmethod
    def _build_error_response(request_id: Any, code: int, message: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }

    async def _write_response(self, response: Dict[str, Any]) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._print_response, response)

    @staticmethod
    def _print_response(response: Dict[str, Any]) -> None:
        print(json.dumps(response), flush=True)


async def run_stdio_server(server: NotionMCPServer) -> None:
    stdio_server = MCPStdIOServer(server)
    await stdio_server.run()
