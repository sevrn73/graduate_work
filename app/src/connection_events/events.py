import aioredis
from connection_events import postgres, redis
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine


async def create_pg_connection():
    postgres.async_pg_engine = create_async_engine(
        f"postgresql+asyncpg://"
        f"{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


async def create_redis_connection():
    redis.redis_client = await aioredis.create_redis_pool(
        f"{settings.REDIS_HOST}://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
    )


async def close_pg_connection():
    await postgres.async_pg_engine.dispose()


async def close_redis_connection():
    await redis.redis_client.wait_closed()


on_startup = [create_pg_connection, create_redis_connection]
on_shutdown = [close_pg_connection, close_redis_connection]
