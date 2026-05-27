import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/elevora"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={
        "statement_cache_size": 0
    },
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    from utils.logger import logger
    from sqlalchemy import text
    import models.database_models

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

            try:
                await conn.execute(
                    text("ALTER TABLE resume_analysis ADD COLUMN filename VARCHAR;")
                )
            except Exception:
                pass

            try:
                await conn.execute(
                    text("ALTER TABLE resume_analysis ADD COLUMN role_matches JSONB;")
                )
            except Exception:
                pass

        logger.info("Database tables verified/created successfully.")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")