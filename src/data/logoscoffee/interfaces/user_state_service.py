from abc import ABC, abstractmethod
from src.data.logoscoffee.entities.user_state_entities import UserData


class UserStateService(ABC):

    @abstractmethod
    async def set_state(self, user_data: UserData, state: str | None):
        """
        :param user_data:
        :param state:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_state(self, user_data: UserData) -> str | None:
        """
        :param user_data:
        :return: The state of the user
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def set_data(self, user_data: UserData, data: dict):
        """
        :param user_data:
        :param data:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_data(self, user_data: UserData) -> dict:
        """
        :param user_data:
        :return: The dict with user state data
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass
