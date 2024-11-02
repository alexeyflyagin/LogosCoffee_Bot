from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import config


class LogosCoffeeDatabase:
    def __init__(self, url: str):
        self.engine = create_async_engine(url)
        self.session_factory = async_sessionmaker(self.engine)
        logger.info(f"Connected to the database.")

    async def disconnect(self):
        await self.engine.dispose()
        logger.info(f"Disconnected from the database.")


database = LogosCoffeeDatabase(config.DB_URL)
