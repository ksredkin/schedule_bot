import os

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "123"

import pytest


@pytest.mark.asyncio
async def test_set_and_get_changes_from_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.changes_cache.r", fake_redis)

    from src.bot.utils.changes_cache import get_changes_from_cache, set_changes_in_cache

    test_data = {"01.01.01": {"10A": [{"Математика": "Нет"}]}}

    await set_changes_in_cache(test_data)
    result = await get_changes_from_cache()

    assert result == test_data


@pytest.mark.asyncio
async def test_get_changes_from_empty_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.changes_cache.r", fake_redis)

    from src.bot.utils.changes_cache import get_changes_from_cache

    result = await get_changes_from_cache()
    assert result is None
