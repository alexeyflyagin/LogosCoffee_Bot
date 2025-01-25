from src.loggers import service_logger as logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.data.logoscoffee.session_manager import SessionManager


class SessionManagerImpl(SessionManager):
    def __init__(self, sqlalchemy_url: str, base_url: str):
        self._engine = create_async_engine(sqlalchemy_url)
        super().__init__(async_sessionmaker(self._engine), base_url)
        logger.info(f"Connected to the database.")

    async def disconnect(self):
        await self._engine.dispose()
        logger.info(f"Disconnected from the database.")
