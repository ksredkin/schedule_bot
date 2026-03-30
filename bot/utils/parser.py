from bs4 import BeautifulSoup
from utils.logger import Logger

logger = Logger(__name__).get_logger()


def parse_schedule(html: str) -> dict | None:
    try:
        soup = BeautifulSoup(html, "lxml")

        table = soup.find("table", class_="rasp")
        rows = table.find_all("tr")

        result = {}

        current_day = None
        current_lesson = None

        for row in rows:
            if row.find("h3"):
                current_day = row.getText(strip=True)
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

            if number:
                current_lesson = int(number)

                result[current_day][current_lesson] = {
                    "time": time,
                    "name": name,
                    "group": group or None,
                    "cab": cab,
                }

            else:
                if current_lesson is None:
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
        url = li.find("a")["href"]

        return url
    except Exception as e:
        logger.critical(f"Не удалось спарсить URL изменений: {e}")
        return None
