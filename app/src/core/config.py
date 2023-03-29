from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Настройки проекта
    """

    PROJECT_NAME: str = "Cinema together API"
    PROJECT_HOST: str = "0.0.0.0"
    PROJECT_PORT: int = Field(8001, env="PROJECT_PORT")
    WS_PORT: int = Field(8002, env="WS_PORT")

    DB_HOST: str = Field("graduate_work_db", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_USER: str = Field("postgres", env="DB_USER")
    DB_PASSWORD: str = Field(1234, env="DB_PASSWORD")
    DB_NAME: str = Field("graduate_work", env="DB_NAME")

    REDIS_HOST: str = Field("redis", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")

    VERIFY_JWT_MODE: bool = Field(False, env="VERIFY_JWT_MODE")
    VERIFY_JWT_URL: str = Field("http://nginx:80/v1/check_perm", env="VERIFY_JWT_URL")


settings = Settings()
