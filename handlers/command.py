from aiogram import Router, types
from aiogram.filters import Command, CommandStart

command_router = Router()

start_message = '''Привет! 👋

Я помогу тебе быстро смотреть <b>расписание ВМЛ</b> 📚

<b>Что я умею:</b>
• 📅 Расписание на сегодня
• 🗓 Расписание на неделю
• 📍 Кабинет текущего урока
• ⏳ Сколько осталось до звонка
• 🔔 Уведомления о заменах

Выбери нужное действие ниже 👇

⚠️ <b>Бот неофициальный</b>
👨‍💻 <b>Автор:</b> @ksredkin'''

@command_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(start_message)