from __future__ import annotations

import environs

from app.utils.singleton import Singleton

env: environs.Env = environs.Env()
env.read_env()


class AppConfig(metaclass=Singleton):
    # App config
    # SERVICE_NAME is set as an environment variable with Terraform
    APP_TITLE: str = env.str("SERVICE_NAME", "app-api")
    APP_API_V1_PREFIX: str = env.str("APP_OPENAPI_V1_PREFIX", "/api/v1")
    APP_OPENAPI_URL: str = env.str(
        "APP_OPENAPI_URL", f"{APP_API_V1_PREFIX}/openapi.json"
    )
    APP_DEBUG: bool = env.bool("APP_DEBUG", False)

    API_DEFAULT_ORDER_BY: str = env.str("API_DEFAULT_ORDER_BY", "created_date")
    API_DEFAULT_ORDER_DIR: str = env.str("API_DEFAULT_ORDER_DIR", "desc")
    API_DEFAULT_LIMIT: int = env.int("API_DEFAULT_LIMIT", 50)
    API_DEFAULT_PAGE: int = env.int("API_DEFAULT_PAGE", 0)
    API_HOST: str = env.str("APP_API_HOST", "localhost")
    API_PORT: str = env.str("APP_API_PORT", "80")

    # DB config
    POSTGRES_USER: str = env.str("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = env.str("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = env.str("POSTGRES_HOST", "")
    POSTGRES_PORT: int = env.int("POSTGRES_PORT", 5432)
    POSTGRES_NAME: str = env.str("POSTGRES_NAME", "")

    # noinspection PyPep8Naming
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if uri := env("SQLALCHEMY_DATABASE_URI", None):
            return uri

        _db_credentials = ""
        if self.POSTGRES_USER and self.POSTGRES_PASSWORD:
            _db_credentials = "{user}:{pwd}".format(
                user=self.POSTGRES_USER, pwd=self.POSTGRES_PASSWORD
            )
        elif self.POSTGRES_USER:
            _db_credentials = self.POSTGRES_USER

        # SQLAlchemy config
        return "postgresql+psycopg2://{credentials}@{host}:{port}/{dbname}".format(
            credentials=_db_credentials,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            dbname=self.POSTGRES_NAME,
        )

    SQLALCHEMY_POOL_SIZE: int = env.int("SQLACLHEMY_POOL_SIZE", 10)

    # Redis config
    REDIS_HOST: str = env.str("REDIS_HOST", "localhost")
    REDIS_PORT: int = env.int("REDIS_PORT", 6379)
    REDIS_USER: str = env.str("REDIS_USER", "")
    REDIS_PASS: str = env.str("REDIS_PASS", "")

    # noinspection PyPep8Naming
    @property
    def CELERY_BROKER_URI(self):
        if uri := env("CELERY_BROKER_URI", None):
            return uri

        _redis_credentials = ""
        if self.REDIS_USER and self.REDIS_PASS:
            _redis_credentials = f"{self.REDIS_USER}:{self.REDIS_PASS}"
        elif self.REDIS_USER:
            _redis_credentials = self.REDIS_USER

        return "redis://{credentials}{host}:{port}".format(
            credentials=f"{_redis_credentials}@" if _redis_credentials else "",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        )

    def __repr__(self):
        return "\n".join(
            [f"{k}: {getattr(self, k)}" for k in dir(self) if not k.startswith("_")]
        )

    def __str__(self):
        return repr(self)


config = AppConfig()
