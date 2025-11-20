"""Data service layer for Theatre operations using SQLAlchemy ORM."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.models import Theatre
from database import get_db


class TheatreDataService:
    """Service layer for Theatre data operations"""

    def get_all_theatres(self, db: Session) -> List[Theatre]:
        """Retrieve all non-deleted theatres from database."""
        return db.query(Theatre).filter(Theatre.is_deleted == False).all()

    def get_theatre_by_id(self, db: Session, theatre_id: int) -> Optional[Theatre]:
        """Retrieve a specific theatre by ID."""
        return db.query(Theatre).filter(
            and_(
                Theatre.theatre_id == theatre_id,
                Theatre.is_deleted == False
            )
        ).first()

    def get_theatres_by_cinema(self, db: Session, cinema_id: int) -> List[Theatre]:
        """Retrieve all theatres for a specific cinema."""
        return db.query(Theatre).filter(
            and_(
                Theatre.cinema_id == cinema_id,
                Theatre.is_deleted == False
            )
        ).all()

    def create_theatre(
        self,
        db: Session,
        cinema_id: int,
        name: str,
        address: str,
        screen_count: int,
        created_by: int
    ) -> Theatre:
        """Create a new theatre."""
        theatre = Theatre(
            cinema_id=cinema_id,
            name=name,
            address=address,
            screen_count=screen_count,
            created_by=created_by
        )
        db.add(theatre)
        db.commit()
        db.refresh(theatre)
        return theatre

    def update_theatre(
        self,
        db: Session,
        theatre_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        screen_count: Optional[int] = None
    ) -> Optional[Theatre]:
        """Update an existing theatre."""
        theatre = self.get_theatre_by_id(db, theatre_id)
        if not theatre:
            return None

        if name is not None:
            theatre.name = name
        if address is not None:
            theatre.address = address
        if screen_count is not None:
            theatre.screen_count = screen_count

        db.commit()
        db.refresh(theatre)
        return theatre

    def delete_theatre(self, db: Session, theatre_id: int) -> bool:
        """Soft delete a theatre."""
        theatre = self.get_theatre_by_id(db, theatre_id)
        if not theatre:
            return False

        theatre.soft_delete()
        db.commit()
        return True
