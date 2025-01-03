from abc import abstractmethod, ABC

from src.data.logoscoffee.entities.orm_entities import OrderEntity


class ClientOrderService(ABC):

    @abstractmethod
    async def get_draft_order(
            self,
            token: str
    ) -> OrderEntity:
        """
        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account

        :return: The draft order entity (if an account exists it is guaranteed that the corresponding draft order also exists)

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def add_to_draft_order(
            self,
            token: str,
            product_id: int
    ):
        """
        Adds a product to the draft order.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account
        :param product_id:

        :raises ProductNotFoundError:
        :raises ProductIsNotAvailableError:
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def remove_from_draft_order(
            self,
            token: str,
            product_id: int
    ):
        """
        It removes a product from the draft order.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account
        :param product_id:

        :raises ProductNotFoundError:
        :raises ProductIsNotAvailableError:
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def clear_draft_order(
            self,
            token: str
    ):
        """
        Removes all products from the draft order.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def place_order(
            self,
            token: str,
            order_id: int | None = None
    ) -> OrderEntity:
        """
        Sends an order to an employee.

        You can send a specific order using `order_id` or draft order if the value of `order_id` is None

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account
        :param order_id:

        :return: The placed order entity

        :raises PlacedOrderIsEmptyError: If order doesn't have products.
        :raises ProductIsNotAvailableError: If order has unavailable products.
        :raises OrderNotFoundError:
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_in_progress_orders(
            self,
            token: str
    ) -> list[OrderEntity]:
        """
        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account

        :return: The list of client's orders entities that have a group of states 'In Progress'.

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_closed_orders(
            self,
            token: str
    ) -> list[OrderEntity]:
        """
        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account

        :return: The list of client's orders entities that have a group of states 'Closed'.

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_product_quantity_in_draft_order(
            self,
            token: str,
            product_id: int
    ) -> int:
        """
        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account
        :param product_id:

        :return: The quantity of the product in the draft order.

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass
