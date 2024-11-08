from abc import ABC, abstractmethod
from typeguard import typechecked
from src.data.logoscoffee.entities.user_state_entities import UserData


class UserStateService(ABC):

    @typechecked
    @abstractmethod
    async def set_state(self, user_data: UserData, state: str | None):
        pass

    @typechecked
    @abstractmethod
    async def get_state(self, user_data: UserData) -> str | None:
        pass

    @typechecked
    @abstractmethod
    async def set_data(self, user_data: UserData, data: dict):
        pass

    @typechecked
    @abstractmethod
    async def get_data(self, user_data: UserData) -> dict:
        pass
