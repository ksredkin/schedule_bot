import os

os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "123"

import pytest


@pytest.mark.asyncio
async def test_set_and_get_image_id_from_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.image_cache.r", fake_redis)

    from src.bot.utils.image_cache import get_image_id_from_cache, set_image_id_in_cache

    test_image = "start"
    test_id = "123"

    await set_image_id_in_cache(test_image, test_id)
    result = await get_image_id_from_cache(test_image)

    assert result == test_id


@pytest.mark.asyncio
async def test_get_image_id_from_empty_cache(mocker, fake_redis):
    mocker.patch("src.bot.utils.image_cache.r", fake_redis)

    from src.bot.utils.image_cache import get_image_id_from_cache

    test_image = "start"

    result = await get_image_id_from_cache(test_image)
    assert result is None
