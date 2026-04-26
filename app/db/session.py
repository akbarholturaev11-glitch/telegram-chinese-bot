from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Backward-compatible alias for older middleware and seed scripts.
SessionLocal = async_session_maker

from app.db.base import Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from app.services.course_seed_service import CourseSeedService

    async with async_session_maker() as session:
        await CourseSeedService(session).sync_all_lessons()
