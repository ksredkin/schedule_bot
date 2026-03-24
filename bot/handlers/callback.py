from aiogram import Router, types
from utils.logger import Logger
from repositories.user_repository import UserRepository
from aiogram import F

callback_router = Router()
logger = Logger(__name__).get_logger()

@callback_router.callback_query(F.data.startswith("set_my_class:"))
async def process_class(callback: types.CallbackQuery):
    grade = callback.data.split(":")[1].lower()
    
    user = await UserRepository.get_user_by_telegram_id(callback.from_user.id)

    if not user:
        await UserRepository.create_user(callback.from_user.id, grade)
    else:
        await UserRepository.update_user_grade(callback.from_user.id, grade)
    
    await callback.message.edit_text("✅ Ваш класс успешно обновлен!")