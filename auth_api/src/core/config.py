from datetime import timedelta
from logging import config as logging_config

from pydantic import BaseModel, BaseSettings, Field
from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class ProjectSettings(BaseSettings):
    SECRET_KEY:str = Field("key", env="SECRET_KEY")


class DbSettings(BaseSettings):
    dbname: str = Field("", env="POSTGRES_NAME")
    user: str = Field("", env="POSTGRES_USER")
    password: str = Field("", env="POSTGRES_PASSWORD")
    host: str = Field("db", env="DB_HOST")
    port: int = Field(5432, env="DB_PORT")


class RedisSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST: str = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    ACCESS_EXPIRES_IN_SECONDS: int = Field(timedelta(hours=1).seconds, env="ACCESS_EXPIRES_IN_SECONDS")
    REFRESH_EXPIRES_IN_SECONDS: int = Field(timedelta(days=90).seconds, env="REFRESH_EXPIRES_IN_SECONDS")
    RATELIMIT_STORAGE_URL: str = Field("redis://redis:6379", env="RATELIMIT_STORAGE_URL")


class JaegerSettings(BaseSettings):
    JAEGER_HOST: str = Field("jaeger", env="JAEGER_HOST")
    JAEGER_PORT: int = Field(6831, env="JAEGER_PORT")
    ENABLE_TRACER: bool = Field(True, env="ENABLE_TRACER")


project_settings = ProjectSettings()
db_settings = DbSettings()
redis_settings = RedisSettings()
jaeger_settings = JaegerSettings()
