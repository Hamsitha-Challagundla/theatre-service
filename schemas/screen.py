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
    num_rows: int = Field(
        ...,
        description="Number of seating rows in the screen.",
        json_schema_extra={"example": 15},
    )
    num_cols: int = Field(
        ...,       
        description="Number of seating columns in the screen.",
        json_schema_extra={"example": 20},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_number": 1,
                    "num_rows": 15,
                    "num_cols": 20,
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
                    "num_rows": 10, 
                    "num_cols": 25,
                }
            ]
        }
    }


class ScreenUpdate(BaseModel):
    """Partial update for a Screen; supply only fields to change."""
    theatre_id: Optional[UUID] = Field(None, description="ID of the theatre this screen belongs to")    
    screen_number: Optional[int] = Field(None, description="Screen number")
    num_rows: Optional[int] = Field(None, description="Number of seating rows")
    num_cols: Optional[int] = Field(None, description="Number of seating columns")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"screen_number": 3},
                {"num_rows": 12},
                {"num_cols": 30},
            ]
        }
    }


class ScreenRead(ScreenBase):
    """Server representation returned to clients."""
    screen_id: UUID = Field(
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
                    "screen_id": "88888888-8888-4888-8888-888888888888",
                    "theatre_id": "99999999-9999-4999-8999-999999999999",
                    "screen_number": 1,
                    "num_rows": 15,
                    "num_cols": 20,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
