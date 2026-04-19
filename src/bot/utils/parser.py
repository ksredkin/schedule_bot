from typing import Any, Dict

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.bot.utils.logger import Logger

logger = Logger(__name__).get_logger()


def parse_schedule(html: str) -> Dict[str, Dict[int, Dict[str, Any]]] | None:
    try:
        soup = BeautifulSoup(html, "lxml")

        table = soup.find("table", class_="rasp")

        if not isinstance(table, Tag):
            logger.critical("Не удалось найти таблицу с расписанием")
            return None

        rows = table.find_all("tr")

        result: Dict[str, Dict[int, Dict[str, Any]]] = {}

        current_day: str | None = None
        current_lesson: int | None = None

        for row in rows:
            if row.find("h3"):
                current_day = row.getText(strip=True)
                if current_day:
                    result[current_day] = {}
                continue

            tds = row.find_all("td")

            if len(tds) != 5:
                continue

            number = tds[0].get_text(strip=True)
            time = tds[1].get_text()
            name = tds[2].get_text()
            group = tds[3].get_text(strip=True)
            cab = tds[4].get_text(strip=True)

            if number and current_day:
                current_lesson = int(number)

                result[current_day][current_lesson] = {
                    "time": time,
                    "name": name,
                    "group": group or None,
                    "cab": cab,
                }

            else:
                if current_lesson is None or current_day is None:
                    continue

                lesson = result[current_day][current_lesson]

                if "groups" not in lesson:
                    lesson["groups"] = []

                lesson["groups"].append({"group": group, "cab": cab})

        return result
    except Exception as e:
        logger.critical(f"Не удалось спарсить расписание: {e}")
        return None


def parse_changes_url(html: str) -> str | None:
    try:
        soup = BeautifulSoup(html, "lxml")

        li = soup.find(
            "li",
            class_="menu-item menu-item-type-custom menu-item-object-custom menu-item-5101",
        )
        if not isinstance(li, Tag):
            logger.critical("Не удалось найти элемент с URL изменений")
            return None

        a_tag = li.find("a")
        if not isinstance(a_tag, Tag):
            logger.critical("Не удалось найти ссылку с URL изменений")
            return None

        url = a_tag.get("href")

        if not isinstance(url, str):
            logger.critical("Не удалось найти URL изменений")
            return None

        return url
    except Exception as e:
        logger.critical(f"Не удалось спарсить URL изменений: {e}")
        return None
