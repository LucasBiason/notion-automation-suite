"""
Date and timezone formatters for Notion API

All dates are formatted to GMT-3 (São Paulo timezone) as required.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple, Union

import pytz

# São Paulo timezone (GMT-3)
SAO_PAULO_TZ = pytz.timezone("America/Sao_Paulo")


def format_date_gmt3(dt: datetime, include_time: bool = True) -> str:
    """
    Format datetime to GMT-3 for Notion API

    Args:
        dt: datetime object to format
        include_time: If True, includes time (HH:MM:SS), else only date (YYYY-MM-DD)

    Returns:
        Formatted string for Notion API

    Examples:
        >>> format_date_gmt3(datetime(2025, 10, 22, 19, 0))
        '2025-10-22T19:00:00-03:00'

        >>> format_date_gmt3(datetime(2025, 10, 22), include_time=False)
        '2025-10-22'
    """
    dt = SAO_PAULO_TZ.localize(dt) if dt.tzinfo is None else dt.astimezone(SAO_PAULO_TZ)

    if include_time:
        return dt.strftime("%Y-%m-%dT%H:%M:%S-03:00")
    else:
        return dt.strftime("%Y-%m-%d")


def create_period(
    start: Union[datetime, str],
    end: Optional[Union[datetime, str]] = None,
    include_time: bool = True,
) -> dict:
    """
    Create period dict for Notion API

    Args:
        start: Start date/datetime
        end: End date/datetime (optional)
        include_time: Whether to include time in the format

    Returns:
        Dict with 'start' and optionally 'end'

    Examples:
        >>> create_period(datetime(2025, 10, 22, 19, 0), datetime(2025, 10, 22, 21, 0))
        {'start': '2025-10-22T19:00:00-03:00', 'end': '2025-10-22T21:00:00-03:00'}

        >>> create_period(datetime(2025, 10, 22), include_time=False)
        {'start': '2025-10-22'}
    """
    result = {}

    if isinstance(start, str):
        result["start"] = start
    else:
        result["start"] = format_date_gmt3(start, include_time)

    if end:
        if isinstance(end, str):
            result["end"] = end
        else:
            result["end"] = format_date_gmt3(end, include_time)

    return result


def get_study_hours(weekday: int = 0) -> Tuple[int, int]:
    """
    Get study hours for a specific weekday

    Args:
        weekday: 0=Monday, 1=Tuesday, ..., 6=Sunday

    Returns:
        Tuple of (start_hour, end_hour)

    Examples:
        >>> get_study_hours(0)  # Monday
        (19, 21)

        >>> get_study_hours(1)  # Tuesday
        (19.5, 21)  # 19:30 due to medical treatment
    """
    if weekday == 1:  # Tuesday
        return (19.5, 21)  # 19:30-21:00
    return (19, 21)  # Default 19:00-21:00


def calculate_class_end_time(start: datetime, duration_minutes: int) -> datetime:
    """
    Calculate class end time, respecting 21:00 limit

    If class would end after 21:00, it overflows to next business day at 19:00

    Args:
        start: Class start datetime
        duration_minutes: Class duration in minutes

    Returns:
        Class end datetime (might be on a different day if overflow)

    Examples:
        >>> start = datetime(2025, 10, 22, 19, 0)
        >>> calculate_class_end_time(start, 90)  # 1h30
        datetime(2025, 10, 22, 20, 30)  # Normal case

        >>> start = datetime(2025, 10, 22, 20, 0)
        >>> calculate_class_end_time(start, 150)  # 2h30
        # Would be 22:30, but limit is 21:00
        # Overflows to next day at 19:00
    """
    end = start + timedelta(minutes=duration_minutes)

    # Check if exceeds 21:00
    if end.hour > 21 or (end.hour == 21 and end.minute > 0):
        # Overflow to next business day
        next_day = start + timedelta(days=1)
        while next_day.weekday() >= 5:  # Skip Saturday (5) and Sunday (6)
            next_day += timedelta(days=1)

        # Start at 19:00 or 19:30 (if Tuesday)
        start_hour, _ = get_study_hours(next_day.weekday())
        next_start = next_day.replace(
            hour=int(start_hour), minute=int((start_hour % 1) * 60), second=0
        )

        # Calculate remaining time
        remaining = duration_minutes - ((21 - start.hour) * 60 - start.minute)
        return next_start + timedelta(minutes=remaining)

    return end


def get_next_business_day(date: datetime) -> datetime:
    """
    Get next business day (Monday-Friday)

    Args:
        date: Reference date

    Returns:
        Next business day
    """
    next_day = date + timedelta(days=1)
    while next_day.weekday() >= 5:  # Skip Saturday (5) and Sunday (6)
        next_day += timedelta(days=1)
    return next_day


def parse_duration(duration_str: str) -> int:
    """
    Parse duration string to minutes

    Args:
        duration_str: Duration in format 'HH:MM:SS' or 'MM:SS'

    Returns:
        Total minutes

    Examples:
        >>> parse_duration('01:30:00')
        90

        >>> parse_duration('45:30')
        45.5
    """
    parts = duration_str.split(":")

    if len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 60 + minutes + (seconds / 60)
    elif len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes + (seconds / 60)
    else:
        raise ValueError(f"Invalid duration format: {duration_str}")


def format_duration(minutes: Union[int, float]) -> str:
    """
    Format minutes to HH:MM:SS

    Args:
        minutes: Total minutes

    Returns:
        Formatted duration string

    Examples:
        >>> format_duration(90)
        '01:30:00'

        >>> format_duration(45.5)
        '00:45:30'
    """
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    secs = int((minutes % 1) * 60)

    return f"{hours:02d}:{mins:02d}:{secs:02d}"
