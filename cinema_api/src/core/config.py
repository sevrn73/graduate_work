from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Настройки проекта
    """

    project_name: str = "Cinema together API"
    project_host: str = "0.0.0.0"
    project_port: int = Field(8001, env="PROJECT_PORT")
    ws_port: int = Field(8002, env="WS_PORT")

    db_host: str = Field("graduate_work_db", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    postgres_name: str = Field("postgres", env="POSTGRES_NAME")

    redis_host: str = Field("redis", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    verify_jwt_mode: bool = Field(False, env="VERIFY_JWT_MODE")
    verify_jwt_url: str = Field("http://nginx:80/v1/check_perm", env="VERIFY_JWT_URL")


settings = Settings()
