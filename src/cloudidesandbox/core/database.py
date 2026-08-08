from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.cloudidesandbox.core.config import db_config

engine = create_async_engine(db_config.DB_URL)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with sessionmaker() as session:
        yield session
