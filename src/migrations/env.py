import sys

sys.path = ['', '..'] + sys.path[1:]

from sqlalchemy import create_engine


from alembic import context

from src.core.settings.settings import get_settings
from src.models import Base

alembic_config = context.config

settings = get_settings()
# import pdb
# pdb.set_trace()


config_section = alembic_config.get_section(alembic_config.config_ini_section)

target_metadata = Base.metadata
# import pdb
# pdb.set_trace()


def run_migrations_offline(config) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=settings.sqlalchemy.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(config) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(url=settings.sqlalchemy.url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline(config_section)
else:
    run_migrations_online(config_section)

