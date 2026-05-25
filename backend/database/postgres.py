import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/elevora")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    from utils.logger import logger
    from sqlalchemy import text
    # Import models here so they are registered with Base
    import models.database_models
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
            # Safe migration for adding filename column
            try:
                await conn.execute(text("ALTER TABLE resume_analysis ADD COLUMN filename VARCHAR;"))
            except Exception as migrate_err:
                # Expected to fail if column already exists
                pass
                
            # Safe migration for adding role_matches column
            try:
                await conn.execute(text("ALTER TABLE resume_analysis ADD COLUMN role_matches JSONB;"))
            except Exception as migrate_err:
                pass
                
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
