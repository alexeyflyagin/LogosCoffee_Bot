from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import ReviewEntity, PromotionalOfferEntity


class AdminService(ABC):

    @abstractmethod
    async def validate_token(self, token: str | None):
        pass

    @abstractmethod
    async def get_new_reviews(self, last_update: datetime) -> list[ReviewEntity]:
        pass

    @abstractmethod
    async def login(self, token: str | None):
        pass

    @abstractmethod
    async def make_promotional_offer(self, token: str | None, text_content: str | None, preview_photo_url: str | None) -> PromotionalOfferEntity:
        pass

    @abstractmethod
    async def get_promotional_offer(self, token: str | None, offer_id: int) -> PromotionalOfferEntity:
        pass

    @abstractmethod
    async def delete_promotional_offer(self, token: str | None, offer_id: int):
        pass

    @abstractmethod
    async def start_promotional_offer(self, token: str | None, promotional_offer_id: int):
        pass
