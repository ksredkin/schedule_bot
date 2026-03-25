from utils.parser import parse_schedule
from utils.logger import Logger
import httpx

logger = Logger(__name__).get_logger()

class ApiClient:
    @staticmethod
    async def get_grade_schedule(grade: str):
        url = "https://vplicei.org/?page_id=465"
        data = {"KlassRasp": grade}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            html = response.text
        
        return parse_schedule(html)
    
    @staticmethod
    async def get_main_page():
        url = "https://vplicei.org"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            html = response.text
        
        return html
    
    @staticmethod
    async def get_file(url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            html = response.text
        
        return html