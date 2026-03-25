from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
import asyncio
from dotenv import load_dotenv
import os
from aiogram.client.session.aiohttp import AiohttpSession
from handlers.command import command_router
from handlers.callback import callback_router
from core.config import BOT_PHOTO_PATH
from utils.logger import Logger
from messages.common import before_start_description, profile_description
from utils.schedule_cache import ScheduleCache
from aiogram.types import BotCommand

logger = Logger(__name__).get_logger()

bot_commands = [BotCommand(command="schedule", description="📆 Расписание на неделю"),
                BotCommand(command="schedule_today", description="📅 Расписание на сегодня"),
                BotCommand(command="schedule_tomorrow", description="📅 Расписание на завтра"),
                BotCommand(command="bell", description="🔔 Время до звонка"),
                BotCommand(command="set_my_class", description="⚙️ Выбрать класс по умолчанию"),
                ]

async def setup_bot(bot: Bot):
    logger.info("Начата настройка бота")
    
    try:
        await bot.set_my_name("Расписание")
        logger.info("Имя бота обновлено")
    except Exception as e:
        logger.warning(f"Не удалось настроить имя бота: {e}")

    try:
        await bot.set_my_description(before_start_description)
        logger.info("Описание бота до start обновлено")
    except Exception as e:
        logger.warning(f"Не удалось настроить описание до start бота: {e}")

    try:
        await bot.set_my_short_description(profile_description)
        logger.info("Описание бота обновлено")
    except Exception as e:
        logger.warning(f"Не удалось настроить описание бота: {e}")

    try:
        await bot.set_my_commands(bot_commands)
        logger.info("Команды бота обновлены")
    except Exception as e:
        logger.warning(f"Не удалось настроить команды бота: {e}")

    try:
        photo = types.InputProfilePhotoStatic(photo=types.FSInputFile(BOT_PHOTO_PATH))
        await bot.set_my_profile_photo(photo=photo)
        logger.info("Фото бота обновлено")
    except Exception as e:
        logger.warning(f"Не удалось настроить фото бота: {e}")

    logger.info("Настройка бота завершена")

async def start_bot():
    try:
        logger.info("Бот запущен")
        load_dotenv()

        import subprocess
        subprocess.run(["alembic", "upgrade", "head"])

        if os.getenv("PROXY"):
            session = AiohttpSession(proxy=os.getenv("PROXY"))
            bot = Bot(os.getenv("TOKEN"), session, DefaultBotProperties(parse_mode="html"))
        else:
            bot = Bot(os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode="html"))

        await setup_bot(bot)

        cache = ScheduleCache()

        dp = Dispatcher()
        dp.include_router(command_router)
        dp.include_router(callback_router)

        logger.info("Начата работа бота")
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"Работа бота остановлена: {e}")

if __name__ == "__main__":
    asyncio.run(start_bot())