from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, date
from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str = Field(
        ...,
        description="Movie title.",
        json_schema_extra={"example": "The Matrix"},
    )
    description: Optional[str] = Field(
        None,
        description="Movie description or synopsis.",
        json_schema_extra={"example": "A computer hacker learns about the true nature of reality."},
    )
    genre: Optional[str] = Field(
        None,
        description="Movie genre.",
        json_schema_extra={"example": "Action"},
    )
    duration_minutes: int = Field(
        ...,
        description="Movie duration in minutes.",
        json_schema_extra={"example": 136},
    )
    release_date: Optional[date] = Field(
        None,
        description="Movie release date.",
        json_schema_extra={"example": "1999-03-31"},
    )
    rating: Optional[str] = Field(
        None,
        description="Movie rating (PG, PG-13, R, etc.).",
        json_schema_extra={"example": "R"},
    )
    director: Optional[str] = Field(
        None,
        description="Movie director.",
        json_schema_extra={"example": "Lana Wachowski, Lilly Wachowski"},
    )
    cast: Optional[str] = Field(
        None,
        description="Main cast members.",
        json_schema_extra={"example": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss"},
    )
    is_active: bool = Field(
        True,
        description="Whether the movie is currently active.",
        json_schema_extra={"example": True},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "The Matrix",
                    "description": "A computer hacker learns about the true nature of reality.",
                    "genre": "Action",
                    "duration_minutes": 136,
                    "release_date": "1999-03-31",
                    "rating": "R",
                    "director": "Lana Wachowski, Lilly Wachowski",
                    "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
                    "is_active": True,
                }
            ]
        }
    }


class MovieCreate(MovieBase):
    """Creation payload for a Movie."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Inception",
                    "description": "A thief who steals corporate secrets through dream-sharing technology.",
                    "genre": "Sci-Fi",
                    "duration_minutes": 148,
                    "release_date": "2010-07-16",
                    "rating": "PG-13",
                    "director": "Christopher Nolan",
                    "cast": "Leonardo DiCaprio, Marion Cotillard, Tom Hardy",
                    "is_active": True,
                }
            ]
        }
    }


class MovieUpdate(BaseModel):
    """Partial update for a Movie; supply only fields to change."""
    title: Optional[str] = Field(None, description="Movie title")
    description: Optional[str] = Field(None, description="Movie description")
    genre: Optional[str] = Field(None, description="Movie genre")
    duration_minutes: Optional[int] = Field(None, description="Movie duration in minutes")
    release_date: Optional[date] = Field(None, description="Movie release date")
    rating: Optional[str] = Field(None, description="Movie rating")
    director: Optional[str] = Field(None, description="Movie director")
    cast: Optional[str] = Field(None, description="Main cast members")
    is_active: Optional[bool] = Field(None, description="Whether the movie is active")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "The Matrix Reloaded"},
                {"duration_minutes": 138},
                {"is_active": False},
            ]
        }
    }


class MovieRead(MovieBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Movie ID.",
        json_schema_extra={"example": "77777777-7777-4777-7777-777777777777"},
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
                    "id": "77777777-7777-4777-7777-777777777777",
                    "title": "The Matrix",
                    "description": "A computer hacker learns about the true nature of reality.",
                    "genre": "Action",
                    "duration_minutes": 136,
                    "release_date": "1999-03-31",
                    "rating": "R",
                    "director": "Lana Wachowski, Lilly Wachowski",
                    "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
                    "is_active": True,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
