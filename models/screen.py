from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class ScreenBase(BaseModel):
    theatre_id: UUID = Field(
        ...,
        description="ID of the theatre this screen belongs to.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    screen_number: int = Field(
        ...,
        description="Screen number within the theatre.",
        json_schema_extra={"example": 1},
    )
    name: Optional[str] = Field(
        None,
        description="Screen name or identifier.",
        json_schema_extra={"example": "Screen 1 - IMAX"},
    )
    capacity: int = Field(
        ...,
        description="Number of seats in this screen.",
        json_schema_extra={"example": 150},
    )
    screen_type: Optional[str] = Field(
        None,
        description="Type of screen (IMAX, 3D, Standard, etc.).",
        json_schema_extra={"example": "IMAX"},
    )
    is_active: bool = Field(
        True,
        description="Whether the screen is currently active.",
        json_schema_extra={"example": True},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_number": 1,
                    "name": "Screen 1 - IMAX",
                    "capacity": 150,
                    "screen_type": "IMAX",
                    "is_active": True,
                }
            ]
        }
    }


class ScreenCreate(ScreenBase):
    """Creation payload for a Screen."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_number": 2,
                    "name": "Screen 2 - Standard",
                    "capacity": 200,
                    "screen_type": "Standard",
                    "is_active": True,
                }
            ]
        }
    }


class ScreenUpdate(BaseModel):
    """Partial update for a Screen; supply only fields to change."""
    screen_number: Optional[int] = Field(None, description="Screen number")
    name: Optional[str] = Field(None, description="Screen name or identifier")
    capacity: Optional[int] = Field(None, description="Number of seats")
    screen_type: Optional[str] = Field(None, description="Type of screen")
    is_active: Optional[bool] = Field(None, description="Whether the screen is active")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Screen 1 - Updated IMAX"},
                {"capacity": 175},
                {"is_active": False},
            ]
        }
    }


class ScreenRead(ScreenBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Screen ID.",
        json_schema_extra={"example": "88888888-8888-4888-8888-888888888888"},
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
                    "id": "88888888-8888-4888-8888-888888888888",
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_number": 1,
                    "name": "Screen 1 - IMAX",
                    "capacity": 150,
                    "screen_type": "IMAX",
                    "is_active": True,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
