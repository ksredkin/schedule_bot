from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
import asyncio
from dotenv import load_dotenv
import os
from aiogram.client.session.aiohttp import AiohttpSession
from handlers.command import command_router
from core.config import BOT_PHOTO_PATH

profile_description = '''📚 Расписание ВМЛ прямо в Telegram

Показывает уроки, кабинеты и время до звонка

⚠️ Неофициальный бот
👨‍💻 Автор: @ksredkin'''

before_start_description = '''Привет! Это бот для удобного просмотра расписания ВМЛ 📚

Ты сможешь:
• посмотреть расписание на сегодня или неделю
• узнать кабинет текущего урока
• узнать, сколько осталось до звонка
• получать уведомления о заменах

⚠️ Это неофициальный бот

Нажми /start, чтобы начать'''

async def set_up_bot(bot: Bot):
    try:
        await bot.set_my_name("Расписание")
    except Exception as e:
        pass

    try:
        await bot.set_my_description(before_start_description)
    except Exception as e:
        pass

    try:
        await bot.set_my_short_description(profile_description)
    except Exception as e:
        pass

    try:
        photo = types.InputProfilePhotoStatic(photo=types.FSInputFile(BOT_PHOTO_PATH))
        await bot.set_my_profile_photo(photo=photo)
    except Exception as e:
        pass

async def start_bot():
    load_dotenv()

    if os.getenv("PROXY"):
        session = AiohttpSession(proxy=os.getenv("PROXY"))
        bot = Bot(os.getenv("TOKEN"), session, DefaultBotProperties(parse_mode="html"))
    else:
        bot = Bot(os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode="html"))

    await set_up_bot(bot)

    dp = Dispatcher()
    dp.include_router(command_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())