from __future__ import annotations

from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field  
   
class TheatreBase(BaseModel):
    name: str = Field(
        ...,
        description="Theatre name.",
        json_schema_extra={"example": "AMC Times Square"},
    )
    address: str = Field(
        ...,
        description="Theatre address.",
        json_schema_extra={"example": "234 W 42nd St, New York, NY 10036"},
    )

    cinema_id: UUID = Field(
        ...,
        description="ID of the cinema this theatre belongs to.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    screenCount: int = Field(
        ...,
        description="Number of screens in the theatre.",
        json_schema_extra={"example": 10},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "AMC Times Square",
                    "address": "234 W 42nd St",
                    "cinema_id": "99999999-9999-4999-8999-999999999999",
                    "screenCount": 10,
                }
            ]
        }
    }


class TheatreCreate(TheatreBase):
    """Creation payload for a Theatre."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Regal Union Square",
                    "address": "850 Broadway",
                    "cinema_id": "88888888-8888-4888-8888-888888888888",
                    "screenCount": 8,
                }
            ]
        }
    }


class TheatreUpdate(BaseModel):
    """Partial update for a Theatre; supply only fields to change."""
    name: Optional[str] = Field(None, description="Theatre name")
    address: Optional[str] = Field(None, description="Theatre address")
    cinema_id: Optional[UUID] = Field(None, description="ID of the cinema this theatre belongs to")
    screenCount: Optional[int] = Field(None, description="Number of screens in the theatre")


    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "AMC Times Square Updated"},
                {"address": "235 W 42nd St"},
                {"screenCount": 12},    
            ]
        }
    }


class TheatreRead(TheatreBase):
    """Server representation returned to clients."""
    theatre_id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Theatre ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
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
                    "id": "99999999-9999-4999-8999-999999999999",
                    "name": "AMC Times Square",
                    "address": "234 W 42nd St, New York, NY 10036",
                    "cinema_id": "99999999-9999-4999-8999-999999999999",
                    "screenCount": 10,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
