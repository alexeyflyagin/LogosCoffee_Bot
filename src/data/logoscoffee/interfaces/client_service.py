from abc import ABC, abstractmethod
from typeguard import typechecked
from src.data.logoscoffee.entities.client_entities import ClientAuthorizationData

class ClientService(ABC):

    @typechecked
    @abstractmethod
    async def validate_token(self, token: str | None):
        pass

    @typechecked
    @abstractmethod
    async def login(self, phone_number: str) -> ClientAuthorizationData:
        pass

    @typechecked
    @abstractmethod
    async def can_make_review(self, token: str):
        pass


    @typechecked
    @abstractmethod
    async def make_review(self, token: str, text: str):
        pass


