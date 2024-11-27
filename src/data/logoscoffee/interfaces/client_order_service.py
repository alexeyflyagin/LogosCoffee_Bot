from abc import abstractmethod, ABC

from src.data.logoscoffee.entities.orm_entities import OrderEntity


class ClientOrderService(ABC):

    @abstractmethod
    async def get_draft_order(self, client_id: int) -> OrderEntity:
        """
        :param client_id:
        :return: The draft order entity (if an account with `client_id` exists it is guaranteed that the corresponding draft order also exists)
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def add_to_draft_order(self, client_id: int, product_id: int):
        """
        Adds a product to the draft order.

        :param client_id:
        :param product_id:
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def remove_from_draft_order(self, client_id: int, product_id: int):
        """
        Removes a product from the draft order.

        :param client_id:
        :param product_id:
        :raises ProductMissingError:
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def clear_draft_order(self, client_id: int):
        """
        Removes all products from the draft order.

        :param client_id:
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def place_order(self, client_id: int, order_id: int | None = None) -> OrderEntity:
        """
        Sends an order to an employee.

        You can send a specific order using `order_id` or draft order if the value of `order_id` is None

        :param client_id: It's required arg. If `order_id` is None we will use a draft order by `client_id`
        :param order_id:
        :raises PlacedOrderIsEmptyError: If order doesn't have products.
        :raises ProductIsNotAvailableError: If order has unavailable products.
        :raises OrderNotFoundError:
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_in_progress_orders(self, client_id: int) -> list[OrderEntity]:
        """
        :param client_id:
        :return: The list of client's orders entities that have a group of states 'In Progress'.
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_archived_orders(self, client_id: int) -> list[OrderEntity]:
        """
        :param client_id:
        :return: The list of client's orders entities that have a group of states 'Closed'.
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_product_quantity_in_draft_order(self, client_id: int, product_id: int) -> int:
        """
        :param client_id:
        :param product_id:
        :return: The quantity of the product in the draft order.
        :raises ClientAccountNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass