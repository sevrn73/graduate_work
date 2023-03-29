from datetime import timedelta
from logging import config as logging_config

from pydantic import BaseModel, BaseSettings, Field
from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class ProjectSettings(BaseSettings):
    SECRET_KEY = Field("key", env="SECRET_KEY")


class DbSettings(BaseSettings):
    dbname: str = Field("", env="POSTGRES_NAME")
    user: str = Field("", env="POSTGRES_USER")
    password: str = Field("", env="POSTGRES_PASSWORD")
    host: str = Field("db", env="DB_HOST")
    port: int = Field(5432, env="DB_PORT")


class RedisSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT = Field(6379, env="REDIS_PORT")
    ACCESS_EXPIRES_IN_SECONDS = Field(timedelta(hours=1).seconds, env="ACCESS_EXPIRES_IN_SECONDS")
    REFRESH_EXPIRES_IN_SECONDS = Field(timedelta(days=90).seconds, env="REFRESH_EXPIRES_IN_SECONDS")
    RATELIMIT_STORAGE_URL = Field("redis://redis:6379", env="RATELIMIT_STORAGE_URL")


class OAuthYandexSettings(BaseModel):
    ID: str = Field("b7835873699d4da8bdb3f5736313e1e7", env="YANDEX_ID")
    SECRET: str = Field("25f1a435daa1477ea32a66b9c0b9e75b", env="YANDEX_SECRET")
    REDIRECT_URI: str = Field("http://localhost/v1/oauth_callback/yandex", env="YANDEX_REDIRECT_URI")


class OAuthGoogleSettings(BaseModel):
    ID: str = Field("964793851838-rg0mmuh52okm2vc054v50rbdv0hlj0fg.apps.googleusercontent.com", env="GOOGLE_ID")
    SECRET: str = Field("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", env="GOOGLE_SECRET")
    REDIRECT_URI: str = Field("http://localhost/v1/oauth_callback/google", env="GOOGLE_REDIRECT_URI")


class OAuthSettings(BaseSettings):
    YANDEX: OAuthYandexSettings
    GOOGLE: OAuthGoogleSettings


class JaegerSettings(BaseModel):
    JAEGER_HOST = Field("jaeger", env="JAEGER_HOST")
    JAEGER_PORT = Field(6831, env="JAEGER_PORT")
    ENABLE_TRACER = Field(True, env="JAEGER_PORT")


project_settings = ProjectSettings()
db_settings = DbSettings()
redis_settings = RedisSettings()
yandex_settings = OAuthYandexSettings()
google_settings = OAuthYandexSettings()
oauthservices_settings = OAuthSettings(YANDEX=yandex_settings, GOOGLE=google_settings)

jaeger_settings = JaegerSettings()
