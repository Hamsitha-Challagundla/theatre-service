from unittest.mock import MagicMock
from services.theatre_data_service import TheatreDataService


def test_get_all_theatres():
    db = MagicMock()
    service = TheatreDataService()

    db.query().filter().all.return_value = ["theatre1", "theatre2"]

    result = service.get_all_theatres(db)

    assert result == ["theatre1", "theatre2"]
    db.query.assert_called_once()


def test_get_theatre_by_id_found():
    db = MagicMock()
    service = TheatreDataService()

    db.query().filter().first.return_value = "theatre"

    result = service.get_theatre_by_id(db, 1)

    assert result == "theatre"


def test_get_theatre_by_id_not_found():
    db = MagicMock()
    service = TheatreDataService()

    db.query().filter().first.return_value = None

    result = service.get_theatre_by_id(db, 999)

    assert result is None


def test_create_theatre():
    db = MagicMock()
    service = TheatreDataService()

    theatre_mock = MagicMock()
    service.create_theatre = MagicMock(return_value=theatre_mock)

    theatre = service.create_theatre(
        db=db,
        cinema_id=1,
        name="PVR",
        address="Delhi",
        screen_count=5,
        created_by=10
    )

    assert theatre == theatre_mock


def test_update_theatre_success():
    db = MagicMock()
    service = TheatreDataService()

    theatre = MagicMock()
    service.get_theatre_by_id = MagicMock(return_value=theatre)

    result = service.update_theatre(db, 1, name="New Name")

    assert result == theatre
    assert theatre.name == "New Name"
    db.commit.assert_called_once()


def test_update_theatre_not_found():
    db = MagicMock()
    service = TheatreDataService()

    service.get_theatre_by_id = MagicMock(return_value=None)

    result = service.update_theatre(db, 1, name="New Name")

    assert result is None


def test_delete_theatre_success():
    db = MagicMock()
    service = TheatreDataService()

    theatre = MagicMock()
    service.get_theatre_by_id = MagicMock(return_value=theatre)

    result = service.delete_theatre(db, 1)

    assert result is True
    theatre.soft_delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_theatre_not_found():
    db = MagicMock()
    service = TheatreDataService()

    service.get_theatre_by_id = MagicMock(return_value=None)

    result = service.delete_theatre(db, 1)

    assert result is False
