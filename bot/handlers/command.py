from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from messages.common import start_message
from utils.api_client import ApiClient
from utils.logger import Logger
from utils.schedule_cache import ScheduleCache
from helpers.formatters import get_schedule_message

command_router = Router()
logger = Logger(__name__).get_logger()

@command_router.message(CommandStart())
async def start(message: types.Message):
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /start")
    await message.answer(start_message)

@command_router.message(Command("schedule"))
async def schedule(message: types.Message):
    if len(message.text.split()) == 1:
        grade = message.text.split()[1]
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

    elif len(message.text.split()) == 2:
        grade = message.text.split()[1]
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