from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity, OrderEntity


class EmployeeService(ABC):

    @abstractmethod
    async def get_new_orders(self, last_update: datetime) -> list[OrderEntity]:
        """
        Used for a poll.

        :param last_update: The last time you received updates
        :return: The list of orders whose status changes correspond to the time interval between `last_update` and current_time
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def login(self, key: str) -> EmployeeAccountEntity:
        """
        You can use this method to login for the first time. The second authorization will be incorrect.

        :param key: The secret key
        :return: The employee account entity
        :raises InvalidKeyError: The `key` is incorrect or the account has already been registered
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def accept_order(self, order_id: int):
        """
        Change the order status to 'Accepted'.

        :param order_id:
        :raises OrderStateError: If the order of the states is not being fulfilled.
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def cancel_order(self, order_id: int, cancel_details: str):
        """
        Change the order status to 'Canceled'.

        :param order_id:
        :param cancel_details: The text explains the reasons of cancellation of the order.
        :raises OrderStateError: If the order of the states is not being fulfilled.
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def ready_order(self, order_id: int):
        """
        Change the order status to 'Ready'.

        :param order_id:
        :raises OrderStateError: If the order of the states is not being fulfilled.
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def complete_order(self, order_id: int):
        """
        Change the order status to 'Completed'.

        :param order_id:
        :raises OrderStateError: If the order of the states is not being fulfilled.
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass
