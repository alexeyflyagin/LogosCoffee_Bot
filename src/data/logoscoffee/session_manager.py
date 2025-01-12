from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from abc import ABC, abstractmethod


class SessionManager(ABC):

    def __init__(self, session_maker: async_sessionmaker, base_url):
        self._session_maker = session_maker
        self._base_url = base_url

    def get_session(self) -> AsyncSession:
        return self._session_maker()

    @property
    def base_url(self) -> str:
        return self._base_url

    @abstractmethod
    async def disconnect(self):
        pass
