import os

from redis.asyncio import Redis

host = os.getenv("REDIS_HOST") if os.getenv("REDIS_HOST") else None
port = os.getenv("REDIS_PORT") if os.getenv("REDIS_PORT") else None

if host is None or port is None:
    raise ValueError("REDIS_HOST и REDIS_PORT не установлены в переменных окружения")

r = Redis(host=host, port=int(port), decode_responses=True)
