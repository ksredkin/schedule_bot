import json

from src.bot.redis_client.client import r
from src.bot.utils.logger import Logger

logger = Logger(__name__).get_logger()


async def get_changes_from_cache() -> dict[str, dict[str, list[dict[str, str]]]] | None:
    changes = await r.get("changes")
    if changes is None:
        logger.info("Замены не найдены в кэше")
    else:
        logger.info("Замены найдены в кэше")
    try:
        return json.loads(changes) if changes else None
    except Exception:
        logger.warning("Не удалось распарсить кэш замен, очищаем")
        return None


async def set_changes_in_cache(
    changes: dict[str, dict[str, list[dict[str, str]]]],
) -> None:
    await r.set("changes", json.dumps(changes))
    logger.info("Замены сохранены в кэше")
