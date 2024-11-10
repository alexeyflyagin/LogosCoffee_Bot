from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.admin_entities import ReviewEntity


class AdminService(ABC):

    @abstractmethod
    async def get_new_reviews(self, last_update: datetime) -> list[ReviewEntity]:
        pass

    @abstractmethod
    async def login(self, token: str | None):
        pass


