from abc import ABC, abstractmethod
from src.data.logoscoffee.entities.client_entities import ClientAuthorizationData
from src.data.logoscoffee.entities.orm_entities import PromotionalOfferEntity


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

    async def get_new_offers(self, last_update_time) -> list[PromotionalOfferEntity]:
        pass

    @abstractmethod
    async def make_review(self, token: str | None, text: str):
        pass


