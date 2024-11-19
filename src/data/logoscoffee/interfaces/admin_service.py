from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import ReviewEntity, AnnouncementEntity, AdminAccountEntity


class AdminService(ABC):

    @abstractmethod
    async def get_new_reviews(self, last_update: datetime) -> list[ReviewEntity]:
        pass

    @abstractmethod
    async def login(self, key: str) -> AdminAccountEntity:
        pass

    @abstractmethod
    async def create_announcement(self, text_content: str | None, preview_photo: str | None) -> AnnouncementEntity:
        pass

    @abstractmethod
    async def get_announcement(self, announcement_id: int) -> AnnouncementEntity:
        pass

    @abstractmethod
    async def delete_announcement(self, announcement_id: int):
        pass

    @abstractmethod
    async def distribute_announcement(self, account_id: int, announcement_id: int):
        pass
