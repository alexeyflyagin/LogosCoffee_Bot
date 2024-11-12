from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity


class EmployeeService(ABC):

    @abstractmethod
    async def login(self, key: str | None) -> EmployeeAccountEntity:
        pass


