from redis_client.client import r
from utils.logger import Logger
from core.config import USER_CLASS_CACHE_EXPIRATION_SECONDS

logger = Logger(__name__).get_logger()
NONE_SENTINEL = "__none__"

async def get_user_class_from_cache(telegram_id: int) -> str | bool | None:
    value = await r.get(f"user:{telegram_id}:class")
    if not value:
        logger.info(f"Класс пользователя {telegram_id} не найден в кэше")
        return None
    
    if value == NONE_SENTINEL:
        logger.info(f"Класс пользователя {telegram_id} не установлен: {value}")
        return False
    
    logger.info(f"Класс пользователя {telegram_id} найден в кэше: {value}")
    return value

async def set_user_class_in_cache(telegram_id: int, grade: str) -> None:
    value = grade if grade is not None else NONE_SENTINEL
    await r.set(f"user:{telegram_id}:class", value, ex=USER_CLASS_CACHE_EXPIRATION_SECONDS)
    logger.info(f"Класс пользователя {telegram_id} сохранен в кэше: {value}")
