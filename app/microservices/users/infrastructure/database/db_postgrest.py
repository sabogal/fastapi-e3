"""Infra: Sesión **asíncrona** con PostgreSQL (asyncpg) para FastAPI Users.
- Use esta variante si sus *routers* son async (recomendado).
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Cambie credenciales según su entorno
DATABASE_URL = "postgresql+asyncpg://admin:admin@db:5432/postgres"


Base = declarative_base()
engine = create_async_engine(
DATABASE_URL,
future=True,
echo=False, # Ponga True si quiere ver SQL en consola
pool_pre_ping=True,
)

async_session_maker = sessionmaker(
bind=engine,
class_=AsyncSession,
expire_on_commit=False,
autoflush=False,
autocommit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)