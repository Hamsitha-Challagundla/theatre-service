"""Utility functions for converting database ORM models to Pydantic models."""

from datetime import datetime
from typing import Dict, Any
from uuid import UUID, uuid4

from utils.etag import int_to_uuid


def parse_datetime(value: Any) -> datetime:
    """
    Parse datetime from various formats.

    Args:
        value: Datetime value (datetime object, ISO string, or None)

    Returns:
        datetime: Parsed datetime or current UTC time if None
    """
    if isinstance(value, datetime):
        return value
    elif value:
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
    return datetime.utcnow()


def db_to_uuid(value: Any) -> UUID:
    """
    Convert database ID to UUID.

    Args:
        value: Database ID (int, str, UUID, or None)

    Returns:
        UUID: Converted or generated UUID
    """
    if isinstance(value, int):
        return int_to_uuid(value)
    elif isinstance(value, UUID):
        return value
    elif value:
        return UUID(str(value))
    return uuid4()


def dict_to_theatre_read(db_item: Any) -> Dict[str, Any]:
    """Convert database ORM model to TheatreRead model dict."""
    return {
        "theatre_id": db_to_uuid(db_item.theatre_id),
        "name": db_item.name,
        "address": db_item.address,
        "cinema_id": db_to_uuid(db_item.cinema_id),
        "screenCount": db_item.screen_count,
        "created_at": db_item.created_at,
        "updated_at": db_item.updated_at,
    }


def dict_to_screen_read(db_item: Any) -> Dict[str, Any]:
    """Convert database ORM model to ScreenRead model dict."""
    return {
        "screen_id": db_to_uuid(db_item.screen_id),
        "theatre_id": db_to_uuid(db_item.theatre_id),
        "screen_number": db_item.screen_number,
        "num_rows": db_item.num_rows,
        "num_cols": db_item.num_cols,
        "created_at": db_item.created_at,
        "updated_at": db_item.updated_at,
    }


def dict_to_cinema_read(db_item: Any) -> Dict[str, Any]:
    """Convert database ORM model to CinemaRead model dict."""
    return {
        "cinema_id": db_to_uuid(db_item.cinema_id),
        "name": db_item.name,
        "created_at": db_item.created_at,
        "updated_at": db_item.updated_at,
    }


def dict_to_showtime_read(db_item: Any) -> Dict[str, Any]:
    """Convert database ORM model to ShowtimeRead model dict."""
    return {
        "showtime_id": db_to_uuid(db_item.showtime_id),
        "screen_id": db_to_uuid(db_item.screen_id),
        "movie_id": db_item.movie_id,
        "start_time": db_item.start_time,
        "seats_booked": db_item.seats_booked,
        "created_at": db_item.created_at,
        "updated_at": db_item.updated_at,
    }
