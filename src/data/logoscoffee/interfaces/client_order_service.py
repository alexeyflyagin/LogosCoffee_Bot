from abc import abstractmethod, ABC

from src.data.logoscoffee.entities.orm_entities import OrderEntity


class ClientOrderService(ABC):

    @abstractmethod
    async def get_draft_order(self, client_id: int) -> OrderEntity:
        pass

    @abstractmethod
    async def add_to_draft_order(self, client_id: int, product_id: int):
        pass

    @abstractmethod
    async def remove_from_draft_order(self, client_id: int, product_id: int):
        pass

    @abstractmethod
    async def clear_draft_order(self, client_id: int):
        pass

    @abstractmethod
    async def place_order(self, client_id: int, order_id: int) -> OrderEntity:
        pass

    @abstractmethod
    async def get_current_orders(self, client_id: int) -> list[OrderEntity]:
        pass

    @abstractmethod
    async def get_archived_orders(self, client_id: int) -> list[OrderEntity]:
        pass
