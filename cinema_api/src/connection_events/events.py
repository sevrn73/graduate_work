from connection_events import postgres, redis
from core.config import settings
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import create_async_engine


async def create_pg_connection():
    postgres.async_pg_engine = create_async_engine(
        f"postgresql+asyncpg://"
        f"{settings.postgres_user}:{settings.postgres_password}@{settings.db_host}:{settings.db_port}/{settings.postgres_name}"
    )


async def create_redis_connection():
    pool = ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=0)
    redis.redis_client = Redis(connection_pool=pool)


async def close_pg_connection():
    await postgres.async_pg_engine.dispose()


async def close_redis_connection():
    await redis.redis_client.wait_closed()


on_startup = [create_pg_connection, create_redis_connection]
on_shutdown = [close_pg_connection, close_redis_connection]
