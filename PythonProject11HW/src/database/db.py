from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.conf.config import config


engine = create_async_engine(config.DB_URL, echo=True)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncSession:

    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
