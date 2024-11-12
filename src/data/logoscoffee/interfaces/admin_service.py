from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import ReviewEntity, PromotionalOfferEntity, AdminAccountEntity


class AdminService(ABC):

    @abstractmethod
    async def get_new_reviews(self, last_update: datetime) -> list[ReviewEntity]:
        pass

    @abstractmethod
    async def login(self, key: str) -> AdminAccountEntity:
        pass

    @abstractmethod
    async def create_promotional_offer(self, text_content: str | None, preview_photo: str | None) -> PromotionalOfferEntity:
        pass

    @abstractmethod
    async def get_promotional_offer(self, offer_id: int) -> PromotionalOfferEntity:
        pass

    @abstractmethod
    async def delete_promotional_offer(self, offer_id: int):
        pass

    @abstractmethod
    async def start_promotional_offer(self, promotional_offer_id: int):
        pass
