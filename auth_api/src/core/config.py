from datetime import timedelta
from logging import config as logging_config

from pydantic import BaseSettings, Field
from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class ProjectSettings(BaseSettings):
    secret_key: str = Field("key", env="SECRET_KEY")


class DbSettings(BaseSettings):
    dbname: str = Field("", env="POSTGRES_NAME")
    user: str = Field("", env="POSTGRES_USER")
    password: str = Field("", env="POSTGRES_PASSWORD")
    host: str = Field("db", env="DB_HOST")
    port: int = Field(5432, env="DB_PORT")


class RedisSettings(BaseSettings):
    # Настройки Redis
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    access_expires_in_seconds: int = Field(timedelta(hours=1).seconds, env="ACCESS_EXPIRES_IN_SECONDS")
    refresh_expires_in_seconds: int = Field(timedelta(days=90).seconds, env="REFRESH_EXPIRES_IN_SECONDS")
    ratelimit_storage_url: str = Field("redis://redis:6379", env="RATELIMIT_STORAGE_URL")


project_settings = ProjectSettings()
db_settings = DbSettings()
redis_settings = RedisSettings()
