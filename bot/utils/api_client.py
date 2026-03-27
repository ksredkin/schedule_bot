from utils.logger import Logger
import httpx

logger = Logger(__name__).get_logger()

class ApiClient:
    @staticmethod
    async def get_grade_schedule(grade: str) -> dict|None:
        try:
            url = "https://vplicei.org/?page_id=465"
            data = {"KlassRasp": grade}

            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data)
                html = response.text
            
            return html
        except Exception as e:
            logger.warning(f"Не удалось получить расписание для класса {grade} с сайта школы: {e}")
            return None

    @staticmethod
    async def get_main_page() -> str|None:
        try:
            url = "https://vplicei.org"

            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                html = response.text
            
            return html
        except Exception as e:
            logger.warning(f"Не удалось получить главную страницу сайта школы: {e}")
            return None

    @staticmethod
    async def get_file(url: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                html = response.text
            
            return html
        except Exception as e:
            logger.warning(f"Не удалось получить файл по ссылке: {url} . Ошибка: {e}")