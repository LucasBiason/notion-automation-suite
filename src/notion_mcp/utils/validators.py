"""
Validators for Notion card data

Validates card data before sending to Notion API, ensuring all rules are followed.
"""

import re
from datetime import datetime
from typing import Any, Dict, Optional

from notion_mcp.utils.constants import (
    RELATION_FIELD,
    STATUS_BY_DATABASE,
    DatabaseType,
)


class ValidationError(Exception):
    """Validation error with detailed message"""

    pass


def validate_title(title: str) -> None:
    """
    Validate card title

    Rules:
    - Must not be empty
    - Must not contain emojis (emojis should be in icon property)

    Args:
        title: Card title to validate

    Raises:
        ValidationError: If title is invalid
    """
    if not title or not title.strip():
        raise ValidationError("Title cannot be empty")

    # Check for common emojis that should not be in title
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F9FF"  # Symbols & Pictographs
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F680-\U0001F6FF"  # Transport & Map
        "\U0001F1E0-\U0001F1FF"  # Flags
        "]+",
        flags=re.UNICODE,
    )

    if emoji_pattern.search(title):
        raise ValidationError(
            f"Title contains emojis: '{title}'. "
            "Please use the 'icon' property instead of emojis in title."
        )


def validate_status(status: str, database_type: DatabaseType) -> None:
    """
    Validate status for specific database type

    Args:
        status: Status to validate
        database_type: Type of database

    Raises:
        ValidationError: If status is invalid for this database type
    """
    valid_statuses = STATUS_BY_DATABASE[database_type]

    if status not in valid_statuses:
        raise ValidationError(
            f"Invalid status '{status}' for database {database_type.value}. "
            f"Valid statuses: {', '.join(valid_statuses)}"
        )


def validate_timezone(date_str: str) -> None:
    """
    Validate that datetime string uses GMT-3 timezone

    Args:
        date_str: Date string to validate

    Raises:
        ValidationError: If timezone is not GMT-3
    """
    if "T" in date_str and "-03:00" not in date_str:
        raise ValidationError(
            f"Datetime must use GMT-3 timezone (-03:00): {date_str}. "
            f"Use utils.formatters.format_date_gmt3() to format dates correctly."
        )


def validate_period(period: Dict[str, str], database_type: DatabaseType) -> None:
    """
    Validate period dict

    Args:
        period: Period dict with 'start' and optionally 'end'
        database_type: Type of database

    Raises:
        ValidationError: If period is invalid
    """
    if "start" not in period:
        raise ValidationError("Period must have 'start' field")

    # Validate timezone if datetime
    if "T" in period["start"]:
        validate_timezone(period["start"])

    if "end" in period and "T" in period["end"]:
        validate_timezone(period["end"])

    # Validate end is after start
    if "end" in period:
        try:
            start_dt = datetime.fromisoformat(period["start"].replace("-03:00", ""))
            end_dt = datetime.fromisoformat(period["end"].replace("-03:00", ""))

            if end_dt < start_dt:
                raise ValidationError(
                    f"Period end ({period['end']}) must be after start ({period['start']})"
                )
        except ValueError as e:
            raise ValidationError(f"Invalid date format: {e}") from e


def validate_relation_field(
    data: Dict[str, Any], database_type: DatabaseType, parent_id: Optional[str] = None
) -> None:
    """
    Validate that relation field is correct for database type

    Args:
        data: Card data
        database_type: Type of database
        parent_id: Parent page ID (if creating subitem)

    Raises:
        ValidationError: If relation field is incorrect
    """
    if not parent_id:
        return  # No relation needed if no parent

    correct_field = RELATION_FIELD[database_type]

    # Check if using correct relation field name
    wrong_fields = set(RELATION_FIELD.values()) - {correct_field}
    for wrong_field in wrong_fields:
        if wrong_field.lower().replace(" ", "_") in data:
            raise ValidationError(
                f"Wrong relation field for {database_type.value} database. "
                f"Use '{correct_field}' instead of '{wrong_field}'."
            )


def validate_card_data(
    data: Dict[str, Any], database_type: DatabaseType, parent_id: Optional[str] = None
) -> None:
    """
    Validate complete card data before creating

    Args:
        data: Complete card data
        database_type: Type of database
        parent_id: Parent page ID (if creating subitem)

    Raises:
        ValidationError: If any validation fails
    """
    # Validate title
    if "title" not in data:
        raise ValidationError("Field 'title' is required")
    validate_title(data["title"])

    # Validate status
    if "status" in data:
        validate_status(data["status"], database_type)

    # Validate period if present
    if "periodo" in data:
        validate_period(data["periodo"], database_type)

    # Validate relation field
    validate_relation_field(data, database_type, parent_id)

    # Validate emoji is not in title (should be separate)
    if "emoji" in data and data.get("emoji") in data.get("title", ""):
        raise ValidationError("Emoji should not be in title. Use separate 'emoji' property.")


def validate_study_hours(start: datetime, end: datetime) -> None:
    """
    Validate study hours respect the rules

    Rules:
    - Default: 19:00-21:00
    - Tuesday: 19:30-21:00
    - NEVER after 21:00

    Args:
        start: Class start time
        end: Class end time

    Raises:
        ValidationError: If hours don't respect the rules
    """

    weekday = start.weekday()
    expected_start, max_end = get_study_hours(weekday)

    # Check start time
    start_hour = start.hour + (start.minute / 60)
    if abs(start_hour - expected_start) > 0.1:  # Allow 5 min tolerance
        raise ValidationError(
            f"Study classes should start at {int(expected_start)}:"
            f"{int((expected_start % 1) * 60):02d}. Got {start.strftime('%H:%M')}"
        )

    # Check end time
    if end.hour > max_end or (end.hour == max_end and end.minute > 0):
        raise ValidationError(
            f"Study classes must end before {max_end}:00. "
            f"Class ends at {end.strftime('%H:%M')}. "
            f"Consider splitting into multiple days."
        )


def get_study_hours(weekday: int) -> tuple:
    """Get study hours based on weekday"""

    if weekday == 1:  # Tuesday
        return (19.5, 21)
    return (19, 21)
