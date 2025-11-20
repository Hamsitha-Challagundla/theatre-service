"""Data service layer for Cinema operations using SQLAlchemy ORM."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.models import Cinema


class CinemaDataService:
    """Service layer for Cinema data operations"""

    def get_all_cinemas(self, db: Session) -> List[Cinema]:
        """Retrieve all non-deleted cinemas from database."""
        return db.query(Cinema).filter(Cinema.is_deleted == False).all()

    def get_cinema_by_id(self, db: Session, cinema_id: int) -> Optional[Cinema]:
        """Retrieve a specific cinema by ID."""
        return db.query(Cinema).filter(
            and_(
                Cinema.cinema_id == cinema_id,
                Cinema.is_deleted == False
            )
        ).first()

    def create_cinema(
        self,
        db: Session,
        name: str,
        created_by: int
    ) -> Cinema:
        """Create a new cinema."""
        cinema = Cinema(
            name=name,
            created_by=created_by
        )
        db.add(cinema)
        db.commit()
        db.refresh(cinema)
        return cinema

    def update_cinema(
        self,
        db: Session,
        cinema_id: int,
        name: Optional[str] = None
    ) -> Optional[Cinema]:
        """Update an existing cinema."""
        cinema = self.get_cinema_by_id(db, cinema_id)
        if not cinema:
            return None

        if name is not None:
            cinema.name = name

        db.commit()
        db.refresh(cinema)
        return cinema

    def delete_cinema(self, db: Session, cinema_id: int) -> bool:
        """Soft delete a cinema."""
        cinema = self.get_cinema_by_id(db, cinema_id)
        if not cinema:
            return False

        cinema.soft_delete()
        db.commit()
        return True
