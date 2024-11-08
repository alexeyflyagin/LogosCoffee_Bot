from abc import ABC, abstractmethod
from typeguard import typechecked

class AdminService(ABC):

    @typechecked
    @abstractmethod
    async def login(self, token: str):
        pass


