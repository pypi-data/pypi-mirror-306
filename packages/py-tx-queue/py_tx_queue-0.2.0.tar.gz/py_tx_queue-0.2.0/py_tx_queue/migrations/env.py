import py_tx_queue.env

from logging.config import fileConfig
import os
from py_tx_queue.db.base import Base

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option(
        "sqlalchemy.url",
        os.getenv("PY_TX_QUEUE_DATABASE_URL")
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        prefix="py_tx_queue.sqlalchemy.",
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table="py_tx_queue__alembic_version",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url") or os.getenv("PY_TX_QUEUE_DATABASE_URL")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="py_tx_queue.sqlalchemy.",
        poolclass=pool.NullPool,
        url=url,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            version_table="py_tx_queue__alembic_version",
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
