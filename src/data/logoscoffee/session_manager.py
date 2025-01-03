from sqlalchemy.ext.asyncio import async_sessionmaker
from abc import ABC, abstractmethod


class SessionManager(ABC):

    def __init__(self, session_maker: async_sessionmaker):
        self.get_session = session_maker

    @abstractmethod
    async def disconnect(self):
        pass
