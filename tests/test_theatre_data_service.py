import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Theatre, Base
from services.theatre_data_service import TheatreDataService


# ---------- FIXTURES ----------

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def service():
    return TheatreDataService()


# ---------- TESTS ----------

def test_create_theatre(db_session, service):
    theatre = service.create_theatre(
        db=db_session,
        cinema_id=1,
        name="PVR",
        address="Bangalore",
        screen_count=5,
        created_by=101
    )

    assert theatre.theatre_id is not None
    assert theatre.name == "PVR"
    assert theatre.is_deleted is False


def test_get_all_theatres(db_session, service):
    service.create_theatre(db_session, 1, "INOX", "Delhi", 4, 1)
    service.create_theatre(db_session, 1, "PVR", "Mumbai", 6, 1)

    theatres = service.get_all_theatres(db_session)

    assert len(theatres) == 2


def test_get_theatre_by_id(db_session, service):
    theatre = service.create_theatre(db_session, 1, "Cinepolis", "Pune", 3, 1)

    result = service.get_theatre_by_id(db_session, theatre.theatre_id)

    assert result is not None
    assert result.name == "Cinepolis"


def test_update_theatre(db_session, service):
    theatre = service.create_theatre(db_session, 1, "Old Name", "Chennai", 2, 1)

    updated = service.update_theatre(
        db_session,
        theatre.theatre_id,
        name="New Name",
        screen_count=5
    )

    assert updated.name == "New Name"
    assert updated.screen_count == 5


def test_delete_theatre_soft_delete(db_session, service):
    theatre = service.create_theatre(db_session, 1, "Delete Me", "Hyderabad", 2, 1)

    result = service.delete_theatre(db_session, theatre.theatre_id)

    assert result is True

    deleted = service.get_theatre_by_id(db_session, theatre.theatre_id)
    assert deleted is None


def test_get_theatres_by_cinema(db_session, service):
    service.create_theatre(db_session, 1, "T1", "Addr1", 3, 1)
    service.create_theatre(db_session, 2, "T2", "Addr2", 4, 1)

    theatres = service.get_theatres_by_cinema(db_session, cinema_id=1)

    assert len(theatres) == 1
    assert theatres[0].cinema_id == 1
