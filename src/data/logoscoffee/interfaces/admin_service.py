from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import ReviewEntity, AnnouncementEntity, AdminAccountEntity


class AdminService(ABC):

    @abstractmethod
    async def get_new_reviews(self, last_update: datetime) -> list[ReviewEntity]:
        """
        Used for polling.

        :param last_update: The last time you received updates
        :return: The list of reviews corresponding to the time interval from `last_update` to current_time
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def login(self, key: str) -> AdminAccountEntity:
        """
        You can use this method to login for the first time. The second authorization will be incorrect.

        :param key: The secret key
        :return: The authorization data
        :raises InvalidKey: The `key` is incorrect or the account has already been registered
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def create_announcement(self, text_content: str | None, preview_photo: str | None) -> AnnouncementEntity:
        """
        :param text_content: Raw text
        :param preview_photo: Photo address
        :return: The created announcement entity
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_announcement_by_id(self, announcement_id: int) -> AnnouncementEntity:
        """
        :param announcement_id:
        :return: The announcement entity
        :raises AnnouncementNotFound:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def delete_announcement(self, announcement_id: int):
        """
        :param announcement_id:
        :raises AnnouncementNotFound:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def distribute_announcement(self, account_id: int, announcement_id: int):
        """
        :param account_id: The admin account ID to check for limits
        :param announcement_id:
        :raises CooldownError: The administrator with `account_id` has already distributed an announcement recently
        :raises AnnouncementNotFound:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass
