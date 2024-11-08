from abc import ABC, abstractmethod
from src.data.logoscoffee.entities.client_entities import ClientAuthorizationData

class ClientService(ABC):

    @abstractmethod
    async def validate_token(self, token: str | None):
        pass

    @abstractmethod
    async def login(self, phone_number: str) -> ClientAuthorizationData:
        pass

    @abstractmethod
    async def can_make_review(self, token: str | None):
        pass


    @abstractmethod
    async def make_review(self, token: str | None, text: str):
        pass


