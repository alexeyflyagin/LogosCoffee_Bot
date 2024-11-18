from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity, OrderEntity


class EmployeeService(ABC):

    @abstractmethod
    async def login(self, key: str | None) -> EmployeeAccountEntity:
        pass

    @abstractmethod
    async def get_new_orders(self, last_update_time: datetime) -> list[OrderEntity]:
        pass

    @abstractmethod
    async def accept_order(self, order_id: int):
        pass

    @abstractmethod
    async def cancel_order(self, order_id: int, cancel_details: str):
        pass

    @abstractmethod
    async def start_cook_order(self, order_id: int):
        pass

    @abstractmethod
    async def ready_order(self, order_id: int):
        pass

    @abstractmethod
    async def complete_order(self, order_id: int):
        pass
