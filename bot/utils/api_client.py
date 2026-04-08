import httpx

from core.config import (
    GET_CHANGES_FILE_TIMEOUT,
    GET_MAIN_PAGE_TIMEOUT,
    GET_SCHEDULE_TIMEOUT,
)
from utils.logger import Logger

logger = Logger(__name__).get_logger()


class ApiClient:
    @staticmethod
    async def get_grade_schedule(grade: str) -> str | None:
        try:
            url = "https://vplicei.org/?page_id=465"
            data = {"KlassRasp": grade}

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, data=data, timeout=GET_SCHEDULE_TIMEOUT
                )
                html = response.text

            return html
        except Exception as e:
            logger.warning(
                f"Не удалось получить расписание для класса {grade} с сайта школы: {e}"
            )
            return None

    @staticmethod
    async def get_main_page() -> str | None:
        try:
            url = "https://vplicei.org"

            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=GET_MAIN_PAGE_TIMEOUT)
                html = response.text

            return html
        except Exception as e:
            logger.warning(f"Не удалось получить главную страницу сайта школы: {e}")
            return None

    @staticmethod
    async def get_file(url: str) -> str | None:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, follow_redirects=True, timeout=GET_CHANGES_FILE_TIMEOUT
                )
                html = response.text

            return html
        except Exception as e:
            logger.warning(f"Не удалось получить файл по ссылке: {url} . Ошибка: {e}")
            return None
