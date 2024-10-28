from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src import config


class LogosCoffeeDatabase:
    def __init__(self, url: str):
        self.engine = create_async_engine(url)
        self.session_factory = async_sessionmaker(self.engine)

    async def connect(self):
        self.engine.begin()

    async def disconnect(self):
        await self.engine.dispose()


database = LogosCoffeeDatabase(config.DB_URL)
