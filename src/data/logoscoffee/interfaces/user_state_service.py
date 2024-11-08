from abc import ABC, abstractmethod
from src.data.logoscoffee.entities.user_state_entities import UserData


class UserStateService(ABC):

    @abstractmethod
    async def set_state(self, user_data: UserData, state: str | None):
        pass

    @abstractmethod
    async def get_state(self, user_data: UserData) -> str | None:
        pass

    @abstractmethod
    async def set_data(self, user_data: UserData, data: dict):
        pass

    @abstractmethod
    async def get_data(self, user_data: UserData) -> dict:
        pass
