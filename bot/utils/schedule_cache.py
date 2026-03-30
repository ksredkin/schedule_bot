import asyncio

from core.config import MINUTES_TO_RESET_SCHEDULE_CACHE


class ScheduleCache:
    _instance = None
    cache: dict[str, dict[str, dict[int, dict[str, str | None]]]] = {}

    def __new__(cls) -> ScheduleCache:
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def get(self, grade: str) -> dict[str, dict[int, dict[str, str | None]]] | None:
        return self.cache.get(grade)

    def set(
        self, grade: str, schedule: dict[str, dict[int, dict[str, str | None]]]
    ) -> None:
        if grade not in self.cache:
            self.cache[grade] = schedule
            asyncio.create_task(self.reset_grade(grade))

    async def reset_grade(self, grade: str) -> None:
        await asyncio.sleep(MINUTES_TO_RESET_SCHEDULE_CACHE * 60)
        self.cache.pop(grade)
