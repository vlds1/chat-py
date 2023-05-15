from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from core import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.postgres.url,
    echo=settings.postgres.echo,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
    pool_timeout=settings.postgres.pool_timeout,
    pool_recycle=settings.postgres.pool_recycle,
    pool_pre_ping=settings.postgres.pool_pre_ping,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session():
    async with SessionLocal() as session:
        yield session