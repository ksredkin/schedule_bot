import os

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "123"

import pytest


@pytest.mark.asyncio
async def test_set_and_get_schedule_from_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.schedule_cache.r", fake_redis)

    from src.bot.utils.schedule_cache import (
        get_schedule_from_cache,
        set_schedule_in_cache,
    )

    test_grade = "11А"
    test_schedule = {"Понедельник": {"1": {"name": "Математика"}}}

    await set_schedule_in_cache(test_grade, test_schedule)
    result = await get_schedule_from_cache(test_grade)

    assert result == test_schedule


@pytest.mark.asyncio
async def test_get_schedule_from_empty_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.schedule_cache.r", fake_redis)

    from src.bot.utils.schedule_cache import get_schedule_from_cache

    test_grade = "11А"

    result = await get_schedule_from_cache(test_grade)
    assert result is None
