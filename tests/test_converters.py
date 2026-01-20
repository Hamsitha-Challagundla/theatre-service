from datetime import datetime
from types import SimpleNamespace

from utils.converters import (
    parse_datetime,
    db_to_int,
    dict_to_theatre_read,
    dict_to_screen_read,
    dict_to_cinema_read,
    dict_to_showtime_read,
)


def test_parse_datetime_with_datetime():
    now = datetime.utcnow()
    result = parse_datetime(now)
    assert result == now


def test_parse_datetime_with_iso_string():
    iso = "2024-01-01T10:00:00Z"
    result = parse_datetime(iso)
    assert isinstance(result, datetime)


def test_parse_datetime_with_none():
    result = parse_datetime(None)
    assert isinstance(result, datetime)


def test_db_to_int_with_int():
    assert db_to_int(5) == 5


def test_db_to_int_with_string():
    assert db_to_int("10") == 10


def test_db_to_int_with_none():
    assert db_to_int(None) == 0


def test_db_to_int_with_invalid():
    assert db_to_int("abc") == 0


def test_dict_to_theatre_read():
    db_item = SimpleNamespace(
        theatre_id=1,
        name="PVR",
        address="Delhi",
        cinema_id=2,
        screen_count=5,
        created_at="2024-01-01",
        updated_at="2024-01-02",
    )

    result = dict_to_theatre_read(db_item)

    assert result["theatre_id"] == 1
    assert result["screenCount"] == 5


def test_dict_to_screen_read():
    db_item = SimpleNamespace(
        screen_id=1,
        theatre_id=2,
        screen_number=None,
        num_rows=10,
        num_cols=20,
        created_at="2024-01-01",
        updated_at="2024-01-02",
    )

    result = dict_to_screen_read(db_item)

    assert result["screen_number"] == 0
    assert result["num_rows"] == 10


def test_dict_to_cinema_read():
    db_item = SimpleNamespace(
        cinema_id=1,
        name="INOX",
        created_at="2024-01-01",
        updated_at="2024-01-02",
    )

    result = dict_to_cinema_read(db_item)

    assert result["cinema_id"] == 1
    assert result["name"] == "INOX"


def test_dict_to_showtime_read():
    db_item = SimpleNamespace(
        showtime_id=1,
        screen_id=2,
        movie_id=3,
        price=250,
        start_time="10:00",
        seats_booked=30,
        created_at="2024-01-01",
        updated_at="2024-01-02",
    )

    result = dict_to_showtime_read(db_item)

    assert result["price"] == 250
    assert result["seats_booked"] == 30
