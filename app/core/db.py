from core.config import settings
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_DB="db"
POSTGRES_HOST="127.0.0.1"
POSTGRES_PORT="5432"

DATABASE_URL=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
