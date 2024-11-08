from abc import ABC, abstractmethod

class EmployeeService(ABC):

    @abstractmethod
    async def login(self, token: str | None):
        pass


