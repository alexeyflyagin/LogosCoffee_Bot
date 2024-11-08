from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.data.logoscoffee.session_manager import SessionManager


class SessionManagerImpl(SessionManager):
    def __init__(self, url: str):
        self.engine = create_async_engine(url)
        super().__init__(async_sessionmaker(self.engine))
        logger.info(f"Connected to the database.")

    async def disconnect(self):
        await self.engine.dispose()
        logger.info(f"Disconnected from the database.")
