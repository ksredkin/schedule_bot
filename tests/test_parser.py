from src.bot.utils.parser import parse_changes_url, parse_schedule

test_schedule_html = """<!DOCTYPE html>
<html>
    <body>
        <table class="rasp">
            <tr><td colspan="1"></td></tr>
            <tr><th colspan="1"><h3>Понедельник</h3></th></tr>
            <tr><th>№</th><th>Время</th><th>Урок</th><th>Гр.</th><th align="center">Каб.</th></tr>
            <tr bgcolor="#f9f9f9">
            <td width="10">1</td>
            <td class="rasp">08:00 - 08:40</td>
            <td class="rasp">Разговор о важном</td>
            <td class="rasp" align="center"></td>
            <td class="rasp" align="center">137</td>
            </tr>
        </table>
    </body>
</html>"""

correct_test_schedule = {
    "Понедельник": {
        "1": {
            "time": "08:00 - 08:40",
            "name": "Разговор о важном",
            "group": None,
            "cab": "137",
        }
    }
}

test_changes_html = """<!DOCTYPE html>
<html>
    <body>
        <li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-5101"><a href="https://example.com">Ссылка</a></li>
    </body>
</html>"""


def test_parse_schedule_valid() -> None:
    schedule = parse_schedule(test_schedule_html)
    assert schedule == correct_test_schedule


def test_parse_schedule_invalid() -> None:
    schedule = parse_schedule(None)
    assert schedule is None


def test_parse_changes_url_valid() -> None:
    url = parse_changes_url(test_changes_html)
    assert url == "https://example.com"


def test_parse_changes_url_invalid() -> None:
    url = parse_changes_url(None)
    assert url is None
