from datetime import datetime

import pytz

from src.bot.utils.time_utils import (
    get_current_lesson,
    get_time_to_bell,
    parse_time_range,
)

test_schedule = {
    "Понедельник": {
        1: {
            "time": "08:00 - 08:40",
            "name": "Разговор о важном",
            "group": None,
            "cab": "137",
        },
        2: {"time": "08:50 - 09:30", "name": "Биология", "group": None, "cab": "126"},
        3: {"time": "09:40 - 10:20", "name": "Алгебра", "group": None, "cab": "223"},
        4: {
            "time": "10:40 - 11:20",
            "name": "Иностранный язык",
            "group": "1",
            "cab": "137",
            "groups": [{"group": "2", "cab": "132"}],
        },
        5: {
            "time": "11:30 - 12:10",
            "name": "Русский язык",
            "group": None,
            "cab": "133",
        },
        6: {
            "time": "12:20 - 13:00",
            "name": "Информатика",
            "group": "1",
            "cab": "111",
            "groups": [{"group": "2", "cab": "113"}],
        },
        7: {
            "time": "13:10 - 13:50",
            "name": "Физическая культура",
            "group": None,
            "cab": "м.сп.з.",
        },
    }
}


def test_parse_time_range_valid() -> None:
    start, end = parse_time_range("08:30 - 09:15")

    assert start.hour == 8
    assert start.minute == 30
    assert end.hour == 9
    assert end.minute == 15


def test_parse_time_range_invalid() -> None:
    start, end = parse_time_range("invalid time")

    assert start is None
    assert end is None


def test_get_time_to_bell_valid() -> None:
    now = datetime(2026, 4, 20, 10, 30, tzinfo=pytz.timezone("Europe/Moscow"))
    time_to_bell, lesson = get_time_to_bell(test_schedule, now)

    assert time_to_bell.total_seconds() == 600.0
    assert lesson == test_schedule.get("Понедельник").get(4)


def test_get_time_to_bell_invalid() -> None:
    now = datetime(2026, 4, 20, 10, 30, tzinfo=pytz.timezone("Europe/Moscow"))
    time_to_bell, lesson = get_time_to_bell(None, now)

    assert time_to_bell is None
    assert lesson is None


def test_get_current_lesson_valid() -> None:
    now = datetime(2026, 4, 20, 10, 44, tzinfo=pytz.timezone("Europe/Moscow"))
    lesson = get_current_lesson(test_schedule, now)

    assert lesson == (4, test_schedule.get("Понедельник").get(4))


def test_get_current_lesson_invalid() -> None:
    now = datetime(2026, 4, 20, 10, 44, tzinfo=pytz.timezone("Europe/Moscow"))
    lesson = get_current_lesson(None, now)

    assert lesson == (None, None)
