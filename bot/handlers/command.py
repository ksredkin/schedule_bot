from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from messages.common import start_message
from utils.logger import Logger
from utils.formatters import get_schedule_message, get_schedule_today_message, get_schedule_tomorrow_message, get_lesson_message, get_bell_message, get_next_lesson_message, get_changes_message
from keyboards.inline import create_cancell_inline_keyboard
from repositories.user_repository import UserRepository
from datetime import datetime
from utils.helpers import get_current_lesson, get_time_to_bell, resolve_grade, get_schedule_by_grade, days_map, classes
from utils.changes_cache import ChangesCache
from utils.image_cache import ImageCache
from aiogram.exceptions import TelegramNetworkError

command_router = Router()
logger = Logger(__name__).get_logger()
image_cache = ImageCache()

@command_router.message(CommandStart())
async def start(message: types.Message):
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /start")

    user = await UserRepository.get_user_by_telegram_id(message.from_user.id)

    if not user:
        await UserRepository.create_user(telegram_id=message.from_user.id, grade=None)

    if image_cache.get("start") is None:
        try:
            image = types.FSInputFile("./img/bot.png")
            message = await message.answer_photo(image, caption=start_message)
            image_cache.set("start", message.photo[-1].file_id)
        except TelegramNetworkError:
            logger.warning("Не удалось отправить ответ с фото на /start")
            await message.answer(start_message)
    else:
        await message.answer_photo(image_cache.get("start"), caption=start_message)

@command_router.message(Command("schedule"))
async def schedule(message: types.Message):
    grade = await resolve_grade(message, "schedule")
    
    if not grade:
        return
    
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule для класса {grade}")
    
    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    await message.answer(get_schedule_message(rasp))

@command_router.message(Command("schedule_today"))
async def schedule_today(message: types.Message):
    now = datetime.now()
    current_day = days_map.get(now.weekday())

    if not current_day:
        await message.answer("🏝️ Сегодня выходной!")
        return

    grade = await resolve_grade(message, "schedule_today")

    if not grade:
        return
    
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule_today для класса {grade}")
    
    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    today_schedule = rasp.get(current_day)
    await message.answer(get_schedule_today_message(today_schedule, current_day))

@command_router.message(Command("schedule_tomorrow"))
async def schedule_tomorrow(message: types.Message):
    now = datetime.now()
    day_tomorrow = days_map.get(now.weekday()+1 if now.weekday()+1 != 7 else 0)

    if not day_tomorrow:
        await message.answer("🏝️ Завтра выходной!")
        return

    grade = await resolve_grade(message, "schedule_tomorrow")

    if not grade:
        return
    
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule_tomorrow для класса {grade}")

    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    tomorrow_schedule = rasp.get(day_tomorrow)
    await message.answer(get_schedule_tomorrow_message(tomorrow_schedule, day_tomorrow.lower()))

@command_router.message(Command("lesson"))
async def lesson(message: types.Message):
    now = datetime.now()
    current_day = days_map.get(now.weekday())

    if not current_day:
        await message.answer("🏝️ Сегодня выходной!")
        return

    grade = await resolve_grade(message, "lesson")

    if not grade:
        return
    
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /lesson для класса {grade}")
    
    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    number, lesson = get_current_lesson(rasp)

    if not number or not lesson:
        next_time_to_bell, next_lesson = get_time_to_bell(rasp)

        if not next_lesson:
            await message.answer("🏝️ Сейчас нет уроков.")
            return

        await message.answer("🏝️ Сейчас нет урока.\n\n" + get_next_lesson_message(next_time_to_bell, next_lesson))
        return

    await message.answer(get_lesson_message(number, lesson))

@command_router.message(Command("bell"))
async def bell(message: types.Message):
    now = datetime.now()
    current_day = days_map.get(now.weekday())

    if not current_day:
        await message.answer("🏝️ Сегодня выходной!")
        return

    grade = await resolve_grade(message, "bell")

    if not grade:
        return
    
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /bell для класса {grade}")

    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    time_to_bell, _ = get_time_to_bell(rasp)

    if not time_to_bell:
        await message.answer("🏝️ Сейчас нет уроков.")
        return

    await message.answer(get_bell_message(time_to_bell))

@command_router.message(Command("set_my_class"))
async def set_my_class(message: types.Message):
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /set_my_class")
    buttons = {grade: "set_my_class:"+grade.lower() for grade in classes}
    await message.answer("📃 Выберите Ваш класс из списка:", reply_markup=create_cancell_inline_keyboard(buttons))

@command_router.message(Command("changes"))
async def changes(message: types.Message):
    grade = await resolve_grade(message, "changes")

    if not grade:
        return

    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /changes для класса {grade}")

    changes_cache = ChangesCache()
    table_rows = changes_cache.get()

    if not table_rows:
        await message.answer("🚫 <b>Ошибка:</b> не удалось получить информацию о заменах. Попробуйте позже.")
        return

    await message.answer(get_changes_message(table_rows, grade.lower()))