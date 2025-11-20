"""Data service layer for Screen operations using SQLAlchemy ORM."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.models import Screen


class ScreenDataService:
    """Service layer for Screen data operations"""

    def get_all_screens(self, db: Session) -> List[Screen]:
        """Retrieve all non-deleted screens from database."""
        return db.query(Screen).filter(Screen.is_deleted == False).all()

    def get_screen_by_id(self, db: Session, screen_id: int) -> Optional[Screen]:
        """Retrieve a specific screen by ID."""
        return db.query(Screen).filter(
            and_(
                Screen.screen_id == screen_id,
                Screen.is_deleted == False
            )
        ).first()

    def get_screens_by_theatre(self, db: Session, theatre_id: int) -> List[Screen]:
        """Retrieve all screens for a specific theatre."""
        return db.query(Screen).filter(
            and_(
                Screen.theatre_id == theatre_id,
                Screen.is_deleted == False
            )
        ).all()

    def create_screen(
        self,
        db: Session,
        theatre_id: int,
        screen_number: str,
        num_rows: int,
        num_cols: int,
        created_by: int
    ) -> Screen:
        """Create a new screen."""
        screen = Screen(
            theatre_id=theatre_id,
            screen_number=screen_number,
            num_rows=num_rows,
            num_cols=num_cols,
            created_by=created_by
        )
        db.add(screen)
        db.commit()
        db.refresh(screen)
        return screen

    def update_screen(
        self,
        db: Session,
        screen_id: int,
        screen_number: Optional[str] = None,
        num_rows: Optional[int] = None,
        num_cols: Optional[int] = None
    ) -> Optional[Screen]:
        """Update an existing screen."""
        screen = self.get_screen_by_id(db, screen_id)
        if not screen:
            return None

        if screen_number is not None:
            screen.screen_number = screen_number
        if num_rows is not None:
            screen.num_rows = num_rows
        if num_cols is not None:
            screen.num_cols = num_cols

        db.commit()
        db.refresh(screen)
        return screen

    def delete_screen(self, db: Session, screen_id: int) -> bool:
        """Soft delete a screen."""
        screen = self.get_screen_by_id(db, screen_id)
        if not screen:
            return False

        screen.soft_delete()
        db.commit()
        return True
