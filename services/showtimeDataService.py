"""Data service layer for Showtime operations using SQLAlchemy ORM."""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.models import Showtime


class ShowtimeDataService:
    """Service layer for Showtime data operations"""

    def get_all_showtimes(self, db: Session) -> List[Showtime]:
        """Retrieve all non-deleted showtimes from database."""
        return db.query(Showtime).filter(
            Showtime.is_deleted == False
        ).order_by(Showtime.start_time).all()

    def get_showtime_by_id(self, db: Session, showtime_id: int) -> Optional[Showtime]:
        """Retrieve a specific showtime by ID."""
        return db.query(Showtime).filter(
            and_(
                Showtime.showtime_id == showtime_id,
                Showtime.is_deleted == False
            )
        ).first()

    def get_showtimes_by_screen(self, db: Session, screen_id: int) -> List[Showtime]:
        """Retrieve all showtimes for a specific screen."""
        return db.query(Showtime).filter(
            and_(
                Showtime.screen_id == screen_id,
                Showtime.is_deleted == False
            )
        ).order_by(Showtime.start_time).all()

    def get_showtimes_by_movie(self, db: Session, movie_id: int) -> List[Showtime]:
        """Retrieve all showtimes for a specific movie."""
        return db.query(Showtime).filter(
            and_(
                Showtime.movie_id == movie_id,
                Showtime.is_deleted == False
            )
        ).order_by(Showtime.start_time).all()

    def create_showtime(
        self,
        db: Session,
        screen_id: int,
        movie_id: int,
        start_time: datetime,
        seats_booked: int,
        price: float,
        created_by: int
    ) -> Showtime:
        """Create a new showtime."""
        showtime = Showtime(
            screen_id=screen_id,
            movie_id=movie_id,
            start_time=start_time,
            price=price,
            seats_booked=seats_booked,
            created_by=created_by
        )
        db.add(showtime)
        db.commit()
        db.refresh(showtime)
        return showtime

    def update_showtime(
        self,
        db: Session,
        showtime_id: int,
        movie_id: Optional[int] = None,
        start_time: Optional[datetime] = None,
        seats_booked: Optional[int] = None,
        price: Optional[float] = None
    ) -> Optional[Showtime]:
        """Update an existing showtime."""
        showtime = self.get_showtime_by_id(db, showtime_id)
        if not showtime:
            return None

        if movie_id is not None:
            showtime.movie_id = movie_id
        if start_time is not None:
            showtime.start_time = start_time
        if seats_booked is not None:
            showtime.seats_booked = seats_booked
        if price is not None:
            showtime.price = price

        db.commit()
        db.refresh(showtime)
        return showtime

    def update_seat_count(self, db: Session, showtime_id: int, seat_delta: int) -> Optional[Showtime]:
        """
        Update seat count by a delta (positive for booking, negative for release).
        Returns updated showtime or None if operation failed.
        """
        showtime = self.get_showtime_by_id(db, showtime_id)
        if not showtime:
            return None

        showtime.seats_booked += seat_delta
        db.commit()
        db.refresh(showtime)
        return showtime

    def delete_showtime(self, db: Session, showtime_id: int) -> bool:
        """Soft delete a showtime."""
        showtime = self.get_showtime_by_id(db, showtime_id)
        if not showtime:
            return False

        showtime.soft_delete()
        db.commit()
        return True
