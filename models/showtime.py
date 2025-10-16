from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, date, time
from pydantic import BaseModel, Field


class ShowtimeBase(BaseModel):
    theatre_id: UUID = Field(
        ...,
        description="ID of the theatre.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    screen_id: UUID = Field(
        ...,
        description="ID of the screen.",
        json_schema_extra={"example": "88888888-8888-4888-8888-888888888888"},
    )
    movie_id: UUID = Field(
        ...,
        description="ID of the movie.",
        json_schema_extra={"example": "77777777-7777-4777-7777-777777777777"},
    )
    show_date: date = Field(
        ...,
        description="Date of the show.",
        json_schema_extra={"example": "2025-01-20"},
    )
    show_time: time = Field(
        ...,
        description="Time of the show.",
        json_schema_extra={"example": "19:30:00"},
    )
    price: float = Field(
        ...,
        description="Ticket price for this showtime.",
        json_schema_extra={"example": 15.99},
    )
    available_seats: int = Field(
        ...,
        description="Number of available seats.",
        json_schema_extra={"example": 150},
    )
    total_seats: int = Field(
        ...,
        description="Total number of seats for this showtime.",
        json_schema_extra={"example": 150},
    )
    is_active: bool = Field(
        True,
        description="Whether the showtime is currently active.",
        json_schema_extra={"example": True},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_id": "88888888-8888-4888-8888-888888888888",
                    "movie_id": "77777777-7777-4777-7777-777777777777",
                    "show_date": "2025-01-20",
                    "show_time": "19:30:00",
                    "price": 15.99,
                    "available_seats": 150,
                    "total_seats": 150,
                    "is_active": True,
                }
            ]
        }
    }


class ShowtimeCreate(ShowtimeBase):
    """Creation payload for a Showtime."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_id": "88888888-8888-4888-8888-888888888888",
                    "movie_id": "77777777-7777-4777-7777-777777777777",
                    "show_date": "2025-01-21",
                    "show_time": "14:00:00",
                    "price": 12.99,
                    "available_seats": 200,
                    "total_seats": 200,
                    "is_active": True,
                }
            ]
        }
    }


class ShowtimeUpdate(BaseModel):
    """Partial update for a Showtime; supply only fields to change."""
    show_date: Optional[date] = Field(None, description="Date of the show")
    show_time: Optional[time] = Field(None, description="Time of the show")
    price: Optional[float] = Field(None, description="Ticket price")
    available_seats: Optional[int] = Field(None, description="Number of available seats")
    total_seats: Optional[int] = Field(None, description="Total number of seats")
    is_active: Optional[bool] = Field(None, description="Whether the showtime is active")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"show_time": "20:00:00"},
                {"price": 18.99},
                {"is_active": False},
            ]
        }
    }


class ShowtimeRead(ShowtimeBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Showtime ID.",
        json_schema_extra={"example": "66666666-6666-4666-6666-666666666666"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "66666666-6666-4666-6666-666666666666",
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_id": "88888888-8888-4888-8888-888888888888",
                    "movie_id": "77777777-7777-4777-7777-777777777777",
                    "show_date": "2025-01-20",
                    "show_time": "19:30:00",
                    "price": 15.99,
                    "available_seats": 150,
                    "total_seats": 150,
                    "is_active": True,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
