from abc import ABC, abstractmethod
from typeguard import typechecked

class EmployeeService(ABC):

    @typechecked
    @abstractmethod
    async def login(self, token: str):
        pass


