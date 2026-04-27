import json

from src.bot.core.config import SCHEDULE_CACHE_EXPIRATION_SECONDS
from src.bot.redis_client.client import r
from src.bot.utils.logger import Logger

logger = Logger(__name__).get_logger()


async def get_schedule_from_cache(
    grade: str,
) -> dict[str, dict[str, dict[str, str | None]]] | None:
    schedule = await r.get(f"schedule:{grade}")
    if schedule is None:
        logger.info(f"Расписание для класса {grade} не найдено в кэше")
    else:
        logger.info(f"Расписание для класса {grade} найдено в кэше")
    try:
        return json.loads(schedule) if schedule else None
    except Exception:
        logger.warning("Не удалось распарсить кэш расписания, очищаем")
        return None


async def set_schedule_in_cache(
    grade: str, schedule: dict[str, dict[str, dict[str, str | None]]]
) -> None:
    await r.set(
        f"schedule:{grade}", json.dumps(schedule), ex=SCHEDULE_CACHE_EXPIRATION_SECONDS
    )
    logger.info(f"Расписание для класса {grade} сохранено в кэше")
