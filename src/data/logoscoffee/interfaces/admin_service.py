from abc import ABC, abstractmethod

class AdminService(ABC):

    @abstractmethod
    async def login(self, token: str | None):
        pass


