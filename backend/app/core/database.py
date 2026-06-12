from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .config import settings
import asyncio

# Convert DATABASE_URL for async if needed
if settings.DATABASE_URL.startswith('postgresql://'):
    ASYNC_DATABASE_URL = settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)
elif settings.DATABASE_URL.startswith('sqlite:///'):
    ASYNC_DATABASE_URL = settings.DATABASE_URL.replace('sqlite:///', 'sqlite+aiosqlite:///', 1)
else:
    ASYNC_DATABASE_URL = settings.DATABASE_URL

# Create async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DEBUG
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get async database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Create tables
async def create_tables():
    from app.models import user, portfolio, trade, strategy, market_data
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
