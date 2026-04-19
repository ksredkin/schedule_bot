from aiogram import types

from src.bot.repositories.user_repository import UserRepository
from src.bot.utils.constants import classes
from src.bot.utils.user_class_cache import (
    get_user_class_from_cache,
    set_user_class_in_cache,
)


async def resolve_grade(message: types.Message, command_name: str) -> str | None:
    if not message.text:
        return None

    parts = message.text.split()

    if len(parts) == 1:
        if not message.from_user:
            return None

        user_class = await get_user_class_from_cache(message.from_user.id)

        if user_class is not None:
            if user_class is False:
                await message.answer(
                    f"🚫 <b>Ошибка:</b> не выбран класс. Используйте /set_my_class или /{command_name} {{class}}."
                )
                return None

            return str(user_class)

        user = await UserRepository.get_user_by_telegram_id(message.from_user.id)

        if not user or not user.grade:
            await message.answer(
                f"🚫 <b>Ошибка:</b> не выбран класс. Используйте /set_my_class или /{command_name}"
                + " {class}."
            )
            return None

        grade = str(user.grade)

        await set_user_class_in_cache(message.from_user.id, grade)

        return grade

    elif len(parts) < 4:
        grade = " ".join(parts[1:]).upper()

        if grade not in classes:
            await message.answer("🚫 <b>Ошибка:</b> такого класса нет.")
            return None

        return grade

    else:
        await message.answer(
            f"🚫 <b>Ошибка:</b> неверный формат. Используйте /{command_name}"
            + " {class}."
        )
        return None
