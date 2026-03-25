from datetime import datetime, timezone
from utils.logger import Logger
import pytz

logger = Logger(__name__).get_logger()

days_map = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
}

def parse_time_range(time_str: str):
    start_str, end_str = time_str.split(" - ")

    start = datetime.strptime(start_str, "%H:%M").time()
    end = datetime.strptime(end_str, "%H:%M").time()

    return start, end

def get_current_lesson(schedule: dict):
    now = datetime.now(pytz.timezone('Europe/Moscow')).time()
    today = days_map.get(datetime.now().weekday())

    if not today or today not in schedule:
        return None, None

    for number, lesson in schedule[today].items():
        start, end = parse_time_range(lesson["time"])

        if start <= now <= end:
            return number, lesson

    return None, None

def get_time_to_bell(schedule: dict):
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    today = days_map.get(datetime.now().weekday())

    if not today or today not in schedule:
        return None, None

    lessons = list(schedule[today].items())

    for i, (_, lesson) in enumerate(lessons):
        start, end = parse_time_range(lesson["time"])

        start_dt = now.replace(hour=start.hour, minute=start.minute, second=0)
        end_dt = now.replace(hour=end.hour, minute=end.minute, second=0)

        if start_dt <= now <= end_dt:
            return end_dt - now, lesson

        if i < len(lessons) - 1:
            next_lesson = lessons[i + 1][1]
            next_start, _ = parse_time_range(next_lesson["time"])

            next_start_dt = now.replace(hour=next_start.hour, minute=next_start.minute, second=0)

            if end_dt <= now <= next_start_dt:
                return next_start_dt - now, None

    return None, None