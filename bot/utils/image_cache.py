from core.config import IMAGE_CACHE_EXPIRATION_SECONDS
from redis_client.client import r
from utils.logger import Logger

logger = Logger(__name__).get_logger()


async def get_image_id_from_cache(image: str) -> str | None:
    image_id = await r.get(f"image:{image}")
    if not image_id:
        logger.info(f"ID изображения {image} не найден в кэше")
    else:
        logger.info(f"ID изображения {image} найден в кэше: {image_id}")
    return image_id if image_id else None


async def set_image_id_in_cache(image: str, image_id: str) -> None:
    await r.set(f"image:{image}", image_id, ex=IMAGE_CACHE_EXPIRATION_SECONDS)
    logger.info(f"ID изображения {image} сохранен в кэше: {image_id}")
