from abc import ABC, abstractmethod
from src.data.logoscoffee.entities.orm_entities import PromotionalOfferEntity, ClientAccountEntity


class ClientService(ABC):

    @abstractmethod
    async def login(self, phone_number: str) -> ClientAccountEntity:
        pass

    @abstractmethod
    async def can_create_review(self, account_id: int):
        pass

    async def get_new_offers(self, last_update_time) -> list[PromotionalOfferEntity]:
        pass

    @abstractmethod
    async def create_review(self, account_id: int, text: str):
        pass


