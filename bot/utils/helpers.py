from datetime import datetime, timezone, timedelta
from utils.logger import Logger
import pytz
import csv
from io import StringIO
from aiogram import types
from repositories.user_repository import UserRepository
from utils.schedule_cache import ScheduleCache
from utils.api_client import ApiClient
from utils.parser import parse_schedule

logger = Logger(__name__).get_logger()

days_map = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
}

classes = ["1А", "1Б", "1В", "1Г",
           "2А", "2Б", "2В", "2Г",
           "3А", "3Б", "3В", "3Г", "3Д",
           "4А", "4Б", "4В", "4Г",
           "5А", "5Б", "5В", "5Г", "5Д",
           "6А", "6Б", "6В", "6Г",
           "7А", "7Б", "7В", "7Г", "7Д",
           "8А", "8Б", "8В", "8Г", "8Д", "8 ТЕХ", "8ГУМ", "8Ф/М", "8Х/Б",
           "9А", "9Б", "9В", "9Г", "9Д",
           "10А", "10Б",
           "11А", "11Б",
           ]

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
                return next_start_dt - now, next_lesson

    return None, None

def get_changes(csv_text: str) -> list|None:
    try:
        reader = csv.reader(StringIO(csv_text))
        rows = list(reader)
        return rows
    except Exception as e:
        logger.critical(f"Не удалось спарсить csv файл замен: {e}")
        return None
    
async def resolve_grade(message: types.Message, command_name: str) -> str|None:
    parts = message.text.split()

    if len(parts) == 1:
        user = await UserRepository.get_user_by_telegram_id(message.from_user.id)

        if not user or not user.grade:
            await message.answer(f"🚫 <b>Ошибка:</b> не выбран класс. Используйте /set_my_class или /{command_name}" + " {class}.")
            return None

        return user.grade

    elif len(parts) < 4:
        grade = " ".join(parts[1:]).upper()

        if grade not in classes:
            await message.answer("🚫 <b>Ошибка:</b> такого класса нет.")
            return None

        return grade

    else:
        await message.answer(f"🚫 <b>Ошибка:</b> неверный формат. Используйте /{command_name}" + " {class}.")
        return None
    
async def get_schedule_by_grade(message: types.Message, grade: str) -> dict|None:
    cache = ScheduleCache()
    rasp = cache.get(grade)
    
    if rasp:
        logger.info(f"Расписание для класса {grade} получено из кэша")
        return rasp

    rasp_html = await ApiClient.get_grade_schedule(grade)

    if not rasp_html:
        await message.answer("🚫 Сайт школы недоступен.")
        return None

    rasp = parse_schedule(rasp_html)

    if not rasp:
        await message.answer("🚫 Ошибка парсинга расписания.")
        return None

    cache.set(grade, rasp)
    logger.info(f"Расписание для класса {grade} получено с сайта")

    return rasp