"""
SQLAlchemy ORM models for Theatre Service
"""

from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base, BaseModel


class Cinema(Base, BaseModel):
    """Cinema ORM model"""
    __tablename__ = 'cinemas'

    cinema_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    # Relationships
    theatres = relationship("Theatre", back_populates="cinema")


class Theatre(Base, BaseModel):
    """Theatre ORM model"""
    __tablename__ = 'theatres'

    theatre_id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, ForeignKey('cinemas.cinema_id'), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    screen_count = Column(SmallInteger, nullable=False, default=0)

    # Relationships
    cinema = relationship("Cinema", back_populates="theatres")
    screens = relationship("Screen", back_populates="theatre")


class Screen(Base, BaseModel):
    """Screen ORM model"""
    __tablename__ = 'screens'

    screen_id = Column(Integer, primary_key=True, autoincrement=True)
    theatre_id = Column(Integer, ForeignKey('theatres.theatre_id'), nullable=False)
    screen_number = Column(String(10), nullable=False)
    num_rows = Column(SmallInteger, nullable=False)
    num_cols = Column(SmallInteger, nullable=False)

    # Relationships
    theatre = relationship("Theatre", back_populates="screens")
    showtimes = relationship("Showtime", back_populates="screen")


class Showtime(Base, BaseModel):
    """Showtime ORM model"""
    __tablename__ = 'showtimes'

    showtime_id = Column(Integer, primary_key=True, autoincrement=True)
    screen_id = Column(Integer, ForeignKey('screens.screen_id'), nullable=False)
    movie_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    seats_booked = Column(SmallInteger, nullable=False, default=0)

    # Relationships
    screen = relationship("Screen", back_populates="showtimes")
