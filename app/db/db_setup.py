# for non async
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# for async
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:sTr0ngPass1234@localhost:5432/cloudlevel"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# for async
ASYNC_SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://postgres:sTr0ngPass1234@localhost:5432/cloudlevel"
)
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


# DB utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    async with AsyncSessionLocal() as async_db:
        yield async_db
        await async_db.commit()
