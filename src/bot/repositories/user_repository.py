from sqlalchemy import select

from src.bot.database.connection import session
from src.bot.database.orm_models import User
from src.bot.utils.logger import Logger

logger = Logger(__name__).get_logger()


class UserRepository:
    @staticmethod
    async def get_users() -> list[User] | None:
        async with session() as conn:
            try:
                result = await conn.execute(select(User))
                users = list(result.scalars().all())
                return users
            except Exception as e:
                logger.critical(
                    f"Произошла ошибка при попытке получить всех пользователей из бд: {e}"
                )
                return None

    @staticmethod
    async def get_user_by_telegram_id(telegram_id: int) -> User | None:
        async with session() as conn:
            try:
                result = await conn.execute(
                    select(User).filter(User.telegram_id == telegram_id)
                )
                user = result.scalars().first()
                return user
            except Exception as e:
                logger.critical(
                    f"Произошла ошибка при попытке получить всех пользователей из бд: {e}"
                )
                return None

    @staticmethod
    async def create_user(telegram_id: int, grade: str | None) -> User | None:
        async with session() as conn:
            try:
                user = User(telegram_id=telegram_id, grade=grade)
                conn.add(user)

                await conn.commit()
                await conn.refresh(user)

                return user
            except Exception as e:
                logger.critical(
                    f"Произошла ошибка при попытке создать пользователя в бд: {e}"
                )
                return None

    @staticmethod
    async def update_user_grade(telegram_id: int, grade: str) -> User | None:
        async with session() as conn:
            try:
                result = await conn.execute(
                    select(User).filter(User.telegram_id == telegram_id)
                )
                user = result.scalars().first()

                if not user:
                    return None

                user.grade = grade  # type: ignore

                await conn.commit()
                await conn.refresh(user)

                return user
            except Exception as e:
                logger.critical(
                    f"Произошла ошибка при попытке создать пользователя в бд: {e}"
                )
                return None
