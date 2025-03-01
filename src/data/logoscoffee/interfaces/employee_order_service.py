from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.models import CancelOrderData


class EmployeeOrderService(ABC):

    @abstractmethod
    async def next_order_state(
            self,
            token: str,
            order_id: int,
    ) -> OrderEntity:
        """
        Use this method to move the order to the next state.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the employee account
        :param order_id:

        :return: The order entity

        :raises OrderStateError: If the state of order is incorrect for this operation
        :raises OrderNotFoundError: If the order was not found
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises LCError:
        """

    @abstractmethod
    async def cancel_order(
            self,
            token: str,
            order_id: int,
            data: CancelOrderData,
    ) -> OrderEntity:
        """
        Use this method to cancel an order.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the employee account
        :param order_id:
        :param data:

        :return: The order entity

        :raises OrderStateError: If the order already has a state_group `CLOSED`
        :raises OrderNotFoundError: If the order was not found
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises LCError:
        """

    @abstractmethod
    async def get_order_by_id(
            self,
            token: str,
            order_id: int,
    ) -> OrderEntity:
        """

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the employee account
        :param order_id:

        :return: The order entity

        :raises OrderNotFoundError: If the order was not found
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises LCError:
        """
