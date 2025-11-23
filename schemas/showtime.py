from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ShowtimeBase(BaseModel):
    screen_id: int = Field(
        ...,
        description="ID of the screen where the movie is shown.",
        json_schema_extra={"example": 202},
    )
    movie_id: int = Field(
        ...,
        description="ID of the movie being shown.",
        json_schema_extra={"example": 1001},
    )
    start_time: datetime = Field(
        ...,
        description="Start time of the showtime.",
        json_schema_extra={"example": "2025-01-20T18:30:00Z"},
    )
    price: float = Field(
        ...,
        description="Ticket price for the showtime (float, required).",
        json_schema_extra={"example": 12.50},
    )
    seats_booked: int = Field(
        default=0,
        description="Number of seats currently booked for this showtime.",
        json_schema_extra={"example": 15},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "screen_id": "1",
                    "movie_id": 1001,
                    "start_time": "2025-01-20T18:30:00Z",
                    "price": 12.5,
                    "seats_booked": 0,
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
                    "screen_id": 202,
                    "movie_id": 1001,
                    "start_time": "2025-01-20T18:30:00Z",
                    "price": 12.5,
                }
            ]
        }
    }


class ShowtimeUpdate(BaseModel):
    """Partial update for a Showtime; supply only fields to change."""
    screen_id: Optional[int] = Field(None, description="ID of the screen")
    movie_id: Optional[int] = Field(None, description="ID of the movie")
    start_time: Optional[datetime] = Field(None, description="Start time")
    price: Optional[float] = Field(None, description="Ticket price")
    seats_booked: Optional[int] = Field(None, description="Number of seats booked")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"start_time": "2025-01-20T19:00:00Z"},
                {"seats_booked": 20},
            ]
        }
    }


class ShowtimeRead(ShowtimeBase):
    """Server representation returned to clients."""
    showtime_id: int = Field(
        ...,
        description="Server-generated Showtime ID.",
        json_schema_extra={"example": 401},
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
                    "showtime_id": "1",
                    "screen_id": "1",
                    "movie_id": 1001,
                    "start_time": "2025-01-20T18:30:00Z",
                    "price": 12.5,
                    "seats_booked": 15,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }


class SeatUpdateRequest(BaseModel):
    """Request to update seat count for a showtime."""
    count: int = Field(
        ...,
        description="Number of seats to add (positive) or release (negative).",
        json_schema_extra={"example": 2},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"count": 2},
                {"count": -1},
            ]
        }
    }


class SeatAvailabilityResponse(BaseModel):
    """Response for seat availability check."""
    showtime_id: int = Field(..., description="ID of the showtime")
    screen_id: int = Field(..., description="ID of the screen")
    total_seats: int = Field(..., description="Total number of seats in the screen")
    seats_booked: int = Field(..., description="Number of seats currently booked")
    seats_available: int = Field(..., description="Number of seats available")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "showtime_id": "1",
                    "screen_id": "1",
                    "total_seats": 300,
                    "seats_booked": 15,
                    "seats_available": 285,
                }
            ]
        }
    }
