from datetime import datetime

from aiogram import Router, types
from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import Command, CommandStart

from keyboards.inline import create_cancell_inline_keyboard
from messages.common import start_message
from repositories.user_repository import UserRepository
from services.update_changes_cache_service import parse_changes_table_rows
from utils.changes_cache import get_changes_from_cache
from utils.formatters import (
    get_bell_message,
    get_changes_message,
    get_lesson_message,
    get_next_lesson_message,
    get_schedule_message,
    get_schedule_today_message,
    get_schedule_tomorrow_message,
)
from utils.helpers import (
    classes,
    days_map,
    get_current_lesson,
    get_schedule_by_grade,
    get_time_to_bell,
    resolve_grade,
)
from utils.image_cache import set_image_id_in_cache, get_image_id_from_cache
from utils.logger import Logger
from utils.user_class_cache import set_user_class_in_cache, get_user_class_from_cache

command_router = Router()
logger = Logger(__name__).get_logger()


@command_router.message(CommandStart())
async def start(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /start")

    user_class_in_cache = await get_user_class_from_cache(message.from_user.id)

    if user_class_in_cache is None:
        logger.info(f"Класс пользователя @{message.from_user.username} не найден в кэше")
        user = await UserRepository.get_user_by_telegram_id(message.from_user.id)

        if not user:
            logger.info(f"Пользователь @{message.from_user.username} не найден в базе данных, создается новый пользователь")
            await UserRepository.create_user(telegram_id=message.from_user.id, grade=None)
            await set_user_class_in_cache(message.from_user.id, None)
        else:
            if user.grade:
                logger.info(f"Класс пользователя @{message.from_user.username} найден в базе данных: {user.grade}, сохраняется в кэше")
                await set_user_class_in_cache(message.from_user.id, str(user.grade))
            else:
                logger.info(f"Класс пользователя @{message.from_user.username} не установлен в базе данных")
                await set_user_class_in_cache(message.from_user.id, None)

    elif user_class_in_cache is False:
        logger.info(f"Класс пользователя @{message.from_user.username} установлен как None в кэше")

    if await get_image_id_from_cache("start") is None:
        try:
            image = types.FSInputFile("./img/bot.png")
            message = await message.answer_photo(image, caption=start_message)

            if not message.photo:
                logger.warning("Ответ на /start не содержит фото")
                await message.answer(start_message)
                return

            await set_image_id_in_cache("start", message.photo[-1].file_id)
        except TelegramNetworkError:
            logger.warning("Не удалось отправить ответ с фото на /start")
            await message.answer(start_message)
    else:
        cached_image_id = await get_image_id_from_cache("start")

        if not isinstance(cached_image_id, str):
            logger.warning(
                "Кэш для фото ответа на /start содержит некорректное значение"
            )
            await message.answer(start_message)
            return

        await message.answer_photo(cached_image_id, caption=start_message)


@command_router.message(Command("schedule"))
async def schedule(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    grade = await resolve_grade(message, "schedule")

    if not grade:
        return

    logger.info(
        f"Пользователь @{message.from_user.username} вызвал команду /schedule для класса {grade}"
    )

    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    await message.answer(get_schedule_message(rasp))


@command_router.message(Command("schedule_today"))
async def schedule_today(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    now = datetime.now()
    current_day = days_map.get(now.weekday())

    if not current_day:
        await message.answer("🏝️ Сегодня выходной!")
        return

    grade = await resolve_grade(message, "schedule_today")

    if not grade:
        return

    logger.info(
        f"Пользователь @{message.from_user.username} вызвал команду /schedule_today для класса {grade}"
    )

    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    today_schedule = rasp.get(current_day)

    if not today_schedule:
        await message.answer("🏝️ Сегодня выходной!")
        return

    await message.answer(get_schedule_today_message(today_schedule, current_day))


@command_router.message(Command("schedule_tomorrow"))
async def schedule_tomorrow(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    now = datetime.now()
    day_tomorrow = days_map.get(now.weekday() + 1 if now.weekday() + 1 != 7 else 0)

    if not day_tomorrow:
        await message.answer("🏝️ Завтра выходной!")
        return

    grade = await resolve_grade(message, "schedule_tomorrow")

    if not grade:
        return

    logger.info(
        f"Пользователь @{message.from_user.username} вызвал команду /schedule_tomorrow для класса {grade}"
    )

    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    tomorrow_schedule = rasp.get(day_tomorrow)

    if not tomorrow_schedule:
        await message.answer("🏝️ Завтра выходной!")
        return

    await message.answer(
        get_schedule_tomorrow_message(tomorrow_schedule, day_tomorrow.lower())
    )


@command_router.message(Command("lesson"))
async def lesson(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    now = datetime.now()
    current_day = days_map.get(now.weekday())

    if not current_day:
        await message.answer("🏝️ Сегодня выходной!")
        return

    grade = await resolve_grade(message, "lesson")

    if not grade:
        return

    logger.info(
        f"Пользователь @{message.from_user.username} вызвал команду /lesson для класса {grade}"
    )

    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    number, lesson = get_current_lesson(rasp)

    if not number or not lesson:
        next_time_to_bell, next_lesson = get_time_to_bell(rasp)

        if not next_lesson:
            await message.answer("🏝️ Сейчас нет уроков.")
            return

        if not next_time_to_bell:
            logger.warning("Не удалось определить время до следующего звонка")
            await message.answer(
                "🏝️ Сейчас нет урока, но не удалось определить время до следующего звонка."
            )
            return

        await message.answer(
            "🏝️ Сейчас нет урока.\n\n"
            + get_next_lesson_message(next_time_to_bell, next_lesson)
        )
        return

    await message.answer(get_lesson_message(number, lesson))


@command_router.message(Command("bell"))
async def bell(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    now = datetime.now()
    current_day = days_map.get(now.weekday())

    if not current_day:
        await message.answer("🏝️ Сегодня выходной!")
        return

    grade = await resolve_grade(message, "bell")

    if not grade:
        return

    logger.info(
        f"Пользователь @{message.from_user.username} вызвал команду /bell для класса {grade}"
    )

    rasp = await get_schedule_by_grade(message, grade)

    if not rasp:
        return

    time_to_bell, _ = get_time_to_bell(rasp)

    if not time_to_bell:
        await message.answer("🏝️ Сейчас нет уроков.")
        return

    await message.answer(get_bell_message(time_to_bell))


@command_router.message(Command("set_my_class"))
async def set_my_class(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    logger.info(
        f"Пользователь @{message.from_user.username} вызвал команду /set_my_class"
    )

    buttons = {grade: "set_my_class:" + grade.lower() for grade in classes}

    await message.answer(
        "📃 Выберите Ваш класс из списка:",
        reply_markup=create_cancell_inline_keyboard(buttons),
    )


@command_router.message(Command("changes"))
async def changes(message: types.Message) -> None:
    if not message.from_user:
        logger.warning("Получено сообщение без информации о пользователе")
        return

    grade = await resolve_grade(message, "changes")

    if not grade:
        return

    logger.info(
        f"Пользователь @{message.from_user.username} вызвал команду /changes для класса {grade}"
    )

    changes = await get_changes_from_cache()

    if changes is None:
        await message.answer(
            "🚫 <b>Ошибка:</b> не удалось получить информацию о заменах. Попробуйте позже."
        )
        return
    
    await message.answer(get_changes_message(changes, grade.lower()))
