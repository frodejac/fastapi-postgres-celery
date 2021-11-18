from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import app
from app.db.base import Base
from app.utils.json import dumps

config = context.config
config.set_main_option("sqlalchemy.url", app.config.SQLALCHEMY_DATABASE_URI)

fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Set this option in order to allow us to update JSON blobs in migration scripts using pydantic models, etc.
    cfg = config.get_section(config.config_ini_section)
    cfg["sqlalchemy.json_serializer"] = dumps

    connectable = engine_from_config(
        cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
