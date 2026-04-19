from src.bot.utils.csv_utils import get_changes

csv_changes = """,,,,,
,,,ЗАМЕНЫ УРОКОВ,,
,,,17.04.2026,,
,,,,,
,,,"Марья И.Г.Пт.,17,.04.",,
Урок,Класс,Предмет,Заменяющий преподаватель,Предмет,Кабинет
2,1г,Физк.,Степан Разин.,Физк., 
,,,,,"""

list_changes = [
    ["", "", "", "", "", ""],
    ["", "", "", "ЗАМЕНЫ УРОКОВ", "", ""],
    ["", "", "", "17.04.2026", "", ""],
    ["", "", "", "", "", ""],
    ["", "", "", "Марья И.Г.Пт.,17,.04.", "", ""],
    ["Урок", "Класс", "Предмет", "Заменяющий преподаватель", "Предмет", "Кабинет"],
    ["2", "1г", "Физк.", "Степан Разин.", "Физк.", " "],
    ["", "", "", "", "", ""],
]


def test_get_changes_valid() -> None:
    changes = get_changes(csv_changes)
    assert changes == list_changes


def test_get_changes_invalid() -> None:
    changes = get_changes(None)
    assert changes is None


def test_get_changes_empty_string() -> None:
    changes = get_changes("")
    assert changes == []
