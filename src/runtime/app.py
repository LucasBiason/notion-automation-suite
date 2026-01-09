"""FastMCP application factory for the Notion Automation Suite."""

from __future__ import annotations

import json
import re
from contextlib import asynccontextmanager
from functools import partial
from typing import Any, Dict, Union

import structlog
from mcp.server.fastmcp import FastMCP

from custom import PersonalNotion, StudyNotion, WorkNotion, YoutuberNotion
from services.notion_service import NotionService
from tools import (
    BaseNotionTools,
    PersonalNotionTools,
    StudyNotionTools,
    WorkNotionTools,
    YoutuberNotionTools,
)
from utils import DatabaseType

from .config import NotionConfig, load_config

logger = structlog.get_logger(__name__)

INSTRUCTIONS = (
    "Notion Automation Suite expõe ferramentas oficiais para organizar as bases "
    "Work, Studies, Personal e Youtuber. Siga os padrões já aplicados nos cards "
    "(datas ISO-8601, horários em GMT-3, enumerações fixas). Priorize idempotência, "
    "evite criar duplicidades e sempre preencha os campos obrigatórios antes de "
    "executar uma ação."
)


def create_fastmcp_app() -> FastMCP:
    """Build a FastMCP instance fully wired to the Notion Automation Suite."""
    config = load_config()
    service = NotionService(config.token)

    work_tools = _build_work_tools(service, config)
    study_tools = _build_study_tools(service, config)
    personal_tools = _build_personal_tools(service, config)
    youtuber_tools = _build_youtuber_tools(service, config)
    base_tools = BaseNotionTools(service)

    @asynccontextmanager
    async def _lifespan(_: FastMCP):
        try:
            yield
        finally:
            await service.close()

    app = FastMCP(
        name="Notion Automation Suite",
        instructions=INSTRUCTIONS,
        website_url="https://www.notion.so",
        lifespan=_lifespan,
    )

    _register_tool_set(app, base_tools)
    _register_tool_set(app, work_tools)
    _register_tool_set(app, study_tools)
    _register_tool_set(app, personal_tools)
    _register_tool_set(app, youtuber_tools)
    _register_database_resources(app, service, config.database_ids)

    logger.info("fastmcp_app_ready")
    return app


def _build_work_tools(service: NotionService, config: NotionConfig) -> WorkNotionTools | None:
    work_id = config.database_ids.get(DatabaseType.WORK)
    if not work_id:
        return None
    work_notion = WorkNotion(service, work_id)
    return WorkNotionTools(work_notion)


def _build_study_tools(service: NotionService, config: NotionConfig) -> StudyNotionTools | None:
    study_id = config.database_ids.get(DatabaseType.STUDIES)
    if not study_id:
        return None
    study_notion = StudyNotion(service, study_id)
    return StudyNotionTools(study_notion)


def _build_personal_tools(service: NotionService, config: NotionConfig) -> PersonalNotionTools | None:
    personal_id = config.database_ids.get(DatabaseType.PERSONAL)
    if not personal_id:
        return None
    personal_notion = PersonalNotion(service, personal_id)
    return PersonalNotionTools(personal_notion)


def _build_youtuber_tools(service: NotionService, config: NotionConfig) -> YoutuberNotionTools | None:
    youtuber_id = config.database_ids.get(DatabaseType.YOUTUBER)
    if not youtuber_id:
        return None
    youtuber_notion = YoutuberNotion(service, youtuber_id)
    return YoutuberNotionTools(youtuber_notion)


def _register_tool_set(app: FastMCP, provider: Any | None) -> None:
    if provider is None:
        return

    for definition in provider.get_tools():
        name = definition.get("name")
        if not name:
            continue

        handler = partial(provider.handle_tool_call, name)
        func = _build_tool_callable(name, definition.get("inputSchema", {}), handler)
        func.__doc__ = definition.get("description", "")

        app.add_tool(
            func,
            name=name,
            description=definition.get("description"),
        )


def _parse_complex_arg(value: Any, expected_type: str) -> Any:
    """
    Parse complex arguments that may arrive as malformed strings.

    Handles cases where dict/list arguments are incorrectly serialized
    as strings by attempting JSON parsing and fixing common malformed patterns.
    """
    # If already correct type, return as-is
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return value

    # Only process if expected type is complex
    if expected_type not in ("dict[str, Any]", "list[Any]", "Any"):
        return value

    # If not a string, return as-is
    if not isinstance(value, str):
        return value

    # Try to parse as JSON
    cleaned = value.strip()

    # Skip empty strings
    if not cleaned:
        return None

    # Try direct JSON parsing first
    if cleaned.startswith("{") or cleaned.startswith("["):
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, (dict, list)):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass

    # Try to fix common malformed patterns
    # Pattern 1: "{}'start': '20null" -> {"start": "..."}
    # Pattern 2: "{'key': 'value'}" -> {"key": "value"}
    # Pattern 3: "{}'Data':{}'date':{}'start': 'nullnullnull" -> {"Data": {"date": {"start": "..."}}}
    if "'" in cleaned and ":" in cleaned:
        try:
            # Try to convert Python dict string to JSON
            # Replace single quotes with double quotes (basic fix)
            fixed = cleaned.replace("'", '"')
            # Fix None/null values
            fixed = fixed.replace('None', 'null')
            # Fix malformed patterns like {}'key': -> {"key":
            fixed = re.sub(r'\{\}\'', '{"', fixed)
            fixed = re.sub(r'\'\s*:', '":', fixed)
            # Try to fix nested patterns
            fixed = re.sub(r'\{\}\"', '{"', fixed)

            parsed = json.loads(fixed)
            if isinstance(parsed, (dict, list)):
                return parsed
        except (json.JSONDecodeError, ValueError, Exception):
            # If all parsing attempts fail, log and return None
            logger.warning(
                "malformed_dict_argument_unparseable",
                value=value[:200],  # Log first 200 chars
                expected_type=expected_type
            )
            return None

    # If we get here, it's not a parseable complex type
    return None


def _build_tool_callable(
    tool_name: str,
    schema: Dict[str, Any],
    handler: Any,
) -> Any:
    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))
    func_name = f"{tool_name}_impl".replace("-", "_")

    required_params: list[str] = []
    optional_params: list[str] = []
    field_types: Dict[str, str] = {}
    for field, spec in properties.items():
        annotation = _schema_type_to_annotation(spec)
        field_types[field] = annotation
        if field in required_fields:
            required_params.append(f"{field}: {annotation}")
        else:
            optional_params.append(f"{field}: {annotation} | None = None")

    signature_parts = required_params + optional_params
    signature = ", ".join(signature_parts)
    header = f"async def {func_name}({signature}) -> Any:" if signature else f"async def {func_name}() -> Any:"

    body_lines = [header, "    arguments: dict[str, Any] = {}"]
    for field, spec in properties.items():
        field_type = spec.get("type")
        if isinstance(field_type, list):
            field_type = next((item for item in field_type if item != "null"), field_type[0])

        # Check if this is a complex type that needs parsing
        is_complex = field_type in ("object", "array")
        expected_type = "dict[str, Any]" if field_type == "object" else "list[Any]" if field_type == "array" else "Any"

        if is_complex:
            # Parse complex arguments that may be malformed strings
            if field in required_fields:
                body_lines.append(f"    # Parse {field} (complex type) if needed")
                body_lines.append(f"    {field}_parsed = _parse_complex_arg({field}, '{expected_type}')")
                body_lines.append(f"    if {field}_parsed is None and {field} is not None:")
                body_lines.append(f"        # If parsing failed, try to use original value")
                body_lines.append(f"        {field}_parsed = {field}")
                body_lines.append(f"    arguments['{field}'] = {field}_parsed")
            else:
                body_lines.append(f"    if {field} is not None:")
                body_lines.append(f"        # Parse {field} (complex type) if needed")
                body_lines.append(f"        {field}_parsed = _parse_complex_arg({field}, '{expected_type}')")
                body_lines.append(f"        if {field}_parsed is None:")
                body_lines.append(f"            # If parsing failed, try to use original value")
                body_lines.append(f"            {field}_parsed = {field}")
                body_lines.append(f"        arguments['{field}'] = {field}_parsed")
        else:
            if field in required_fields:
                body_lines.append(f"    arguments['{field}'] = {field}")
            else:
                body_lines.append(f"    if {field} is not None:")
                body_lines.append(f"        arguments['{field}'] = {field}")
    body_lines.append("    return await handler(arguments)")

    namespace: Dict[str, Any] = {
        "Any": Any,
        "Union": Union,
        "handler": handler,
        "_parse_complex_arg": _parse_complex_arg,
        "json": json,
        "logger": logger,
    }
    exec("\n".join(body_lines), namespace)
    func = namespace[func_name]
    return func


def _schema_type_to_annotation(schema: Dict[str, Any]) -> str:
    """
    Convert JSON schema type to Python type annotation.

    For complex types (object, array), we use Union[str, dict/list] to allow
    malformed strings to pass Pydantic validation, then parse them manually.
    """
    type_value = schema.get("type")
    if isinstance(type_value, list):
        type_value = next((item for item in type_value if item != "null"), type_value[0])

    if type_value == "string":
        return "str"
    if type_value == "integer":
        return "int"
    if type_value == "number":
        return "float"
    if type_value == "boolean":
        return "bool"
    if type_value == "array":
        # Use Union to allow both string and list to pass validation
        return "Union[str, list[Any], Any]"
    if type_value == "object":
        # Use Union to allow both string and dict to pass validation
        return "Union[str, dict[str, Any], Any]"

    return "Any"


def _register_database_resources(
    app: FastMCP,
    service: NotionService,
    database_ids: Dict[DatabaseType, str | None],
) -> None:
    for db_type, database_id in database_ids.items():
        if not database_id:
            continue

        uri = f"notion://database/{db_type.value}"
        title = f"{db_type.value.title()} Database"
        description = f"Esquema completo da base {db_type.value}."

        def _register_resource(db_id: str) -> None:
            @app.resource(
                uri,
                name=f"{db_type.value}-database",
                title=title,
                description=description,
                mime_type="application/json",
            )
            async def _read_database() -> Dict[str, Any]:
                return await service.get_database(db_id)

        _register_resource(database_id)


