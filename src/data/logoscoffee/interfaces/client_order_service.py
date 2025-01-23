from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.models import PlaceOrderData


class ClientOrderService(ABC):

    @abstractmethod
    async def can_place_order(
            self,
            token: str,
    ):
        """
        Use it to check the possibility of placing an order.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account

        :raises OtherOrderIsPlacedAlreadyError: If another order has already been placed now
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def place_order(
            self,
            token: str,
            data: PlaceOrderData,
    ) -> OrderEntity:
        """
        Use this method to create an order and send it to an employee.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account
        :param data:

        :raises OtherOrderIsPlacedAlreadyError: If another order has already been placed now
        :raises EmptyTextError: If the order details is empty
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
