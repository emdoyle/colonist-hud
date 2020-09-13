from aioredis import create_redis_pool, Redis
from django.conf import settings


class RedisPool:
    __pool = None

    @classmethod
    async def setup(cls) -> None:
        if cls.__pool is not None:
            return
        cls.__pool = await create_redis_pool(
            address=(settings.REDIS_HOST, settings.REDIS_PORT),
            db=settings.REDIS_MAIN_DB_NO,
        )

    @classmethod
    def get(cls) -> "Redis":
        if cls.__pool is None:
            raise ValueError("RedisPool is not initialized!")
        return cls.__pool
