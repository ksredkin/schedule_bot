from core.config import MINUTES_TO_RESET_SCHEDULE_CACHE
import asyncio

class ScheduleCache:
    _instance = None
    cache = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def get(self, grade: str) -> dict|None:
        return self.cache.get(grade)
    
    def set(self, grade: str, schedule: dict):
        if not grade in self.cache:
            self.cache[grade] = schedule
            asyncio.create_task(self.reset_grade(grade))

    async def reset_grade(self, grade: str):
        await asyncio.sleep(MINUTES_TO_RESET_SCHEDULE_CACHE*60)
        self.cache.pop(grade)