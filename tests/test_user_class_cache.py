import os

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "123"

import pytest


@pytest.mark.asyncio
async def test_get_user_class_from_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.user_class_cache.r", fake_redis)

    from src.bot.utils.user_class_cache import (
        get_user_class_from_cache,
        set_user_class_in_cache,
    )

    test_telegram_id = 123456789
    test_grade = "11А"

    await set_user_class_in_cache(test_telegram_id, test_grade)
    result = await get_user_class_from_cache(test_telegram_id)

    assert result == test_grade


@pytest.mark.asyncio
async def test_get_user_class_from_empty_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.user_class_cache.r", fake_redis)

    from src.bot.utils.user_class_cache import get_user_class_from_cache

    test_telegram_id = 123456789

    result = await get_user_class_from_cache(test_telegram_id)
    assert result is None
