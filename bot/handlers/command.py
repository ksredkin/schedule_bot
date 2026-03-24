from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from messages.common import start_message
from utils.api_client import ApiClient
from utils.logger import Logger
from utils.schedule_cache import ScheduleCache
from helpers.formatters import get_schedule_message, get_schedule_today_message
from keyboards.inline import create_cancell_inline_keyboard
from repositories.user_repository import UserRepository
from datetime import datetime

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

command_router = Router()
logger = Logger(__name__).get_logger()

@command_router.message(CommandStart())
async def start(message: types.Message):
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /start")
    await message.answer(start_message)

@command_router.message(Command("schedule"))
async def schedule(message: types.Message):
    if len(message.text.split()) == 1:
        user = await UserRepository.get_user_by_telegram_id(message.from_user.id)

        if not user:
            await message.answer("🚫 <b>Ошибка:</b> не выбран класс по умолчанию. Используйте /set_my_class для настройки класса по умолчанию или укажите класс в команде: /schedule {class}.")
            return
        
        grade = user.grade

        logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule для класса {grade} (выбран класс по умолчанию)")

        cache = ScheduleCache()
        if cache.get(grade) is None:
            rasp = await ApiClient.get_grade_schedule(grade)
            cache.set(grade, rasp)
            logger.info(f"Расписание для класса {grade} получено с сайта")
        else:
            rasp = cache.get(grade)
            logger.info(f"Расписание для класса {grade} получено из кэша")

        await message.answer(get_schedule_message(rasp))

    elif len(message.text.split()) == 2:
        grade = message.text.lower().split()[1]
        logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule для класса {grade} (указал в команде)")

        cache = ScheduleCache()
        if cache.get(grade) is None:
            rasp = await ApiClient.get_grade_schedule(grade)
            cache.set(grade, rasp)
            logger.info(f"Расписание для класса {grade} получено с сайта")
        else:
            rasp = cache.get(grade)
            logger.info(f"Расписание для класса {grade} получено из кэша")

        await message.answer(get_schedule_message(rasp))

    else:
        await message.answer("🚫 <b>Ошибка:</b> неверный формат команды. Используйте /schedule без аргументов для выбора класса по умолчанию (настраивается в /set_my_class) или /schedule {class} для выбора конкретного класса.")

@command_router.message(Command("schedule_today"))
async def schedule(message: types.Message):
    days_map = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
    }

    now = datetime.now()
    current_day = days_map.get(now.weekday())

    if not current_day:
        await message.answer("🏝️ Сегодня выходной!")
        return

    if len(message.text.split()) == 1:
        user = await UserRepository.get_user_by_telegram_id(message.from_user.id)

        if not user:
            await message.answer("🚫 <b>Ошибка:</b> не выбран класс по умолчанию. Используйте /set_my_class для настройки класса по умолчанию или укажите класс в команде: /schedule {class}.")
            return
        
        grade = user.grade

        logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule_today для класса {grade} (выбран класс по умолчанию)")

    elif len(message.text.split()) == 2:
        grade = message.text.lower().split()[1]
        logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule_today для класса {grade} (указал в команде)")

    else:
        await message.answer("🚫 <b>Ошибка:</b> неверный формат команды. Используйте /schedule без аргументов для выбора класса по умолчанию (настраивается в /set_my_class) или /schedule {class} для выбора конкретного класса.")

    cache = ScheduleCache()
    if cache.get(grade) is None:
        rasp = await ApiClient.get_grade_schedule(grade)
        cache.set(grade, rasp)
        logger.info(f"Расписание для класса {grade} получено с сайта")
    else:
        rasp = cache.get(grade)
        logger.info(f"Расписание для класса {grade} получено из кэша")

    schedule_today = rasp.get(current_day)
    await message.answer(get_schedule_today_message(schedule_today, current_day.lower()))

@command_router.message(Command("set_my_class"))
async def set_my_class(message: types.Message):
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /set_my_class")
    buttons = {grade: "set_my_class:"+grade.lower() for grade in classes}
    await message.answer("📃 Выберите ваш класс из списка:", reply_markup=create_cancell_inline_keyboard(buttons))