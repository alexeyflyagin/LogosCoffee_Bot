from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.orm_entities import OrderEntity


class EmployeeOrderService(ABC):

    @abstractmethod
    async def move_order(
            self,
            token: str,
            order_id: int,
    ) -> OrderEntity:
        """
        Use this method to move the order to the next state.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the employee account
        :param order_id:

        :return: The employee account entity

        :raises OrderStateError: If the order state is unexpected
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
