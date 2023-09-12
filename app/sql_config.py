# used for handling asynchronous database connections and sessions.
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# used to create database sessions.
from sqlalchemy.orm import sessionmaker

# Will used for defining database models.
from sqlmodel import SQLModel

# to initialize the SQLModel metadata from the models
from app.models import hero

# String that specifies the database connection URL for PostgreSQL database URL.
DB_CONFIG = "postgresql+asyncpg://postgres:sTr0ngPass1234@localhost:5432/cloudlevel"


class AsyncDbSession:
    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        self.engine = create_async_engine(DB_CONFIG, future=True, echo=True)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = AsyncDbSession()


async def commit_rollback():
    try:
        await db.commit()
        print("COMMITED")
    except Exception as e:
        print("ERROR: Rollback in progress.", e)
        await db.rollback()
        raise
