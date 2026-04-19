from src.bot.utils.api_client import ApiClient
from src.bot.utils.logger import Logger
from src.bot.utils.parser import parse_schedule
from src.bot.utils.schedule_cache import get_schedule_from_cache, set_schedule_in_cache

logger = Logger(__name__).get_logger()


async def get_schedule_by_grade(
    grade: str,
) -> dict[str, dict[int, dict[str, str | None]]] | None:
    rasp = await get_schedule_from_cache(grade)

    if rasp:
        logger.info(f"Расписание для класса {grade} получено из кэша")
        return rasp

    rasp_html = await ApiClient.get_grade_schedule(grade)

    if not rasp_html:
        return None

    rasp = parse_schedule(rasp_html)

    if not rasp:
        return None

    await set_schedule_in_cache(grade, rasp)
    return rasp
