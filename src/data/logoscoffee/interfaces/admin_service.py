from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import ReviewEntity, AnnouncementEntity, AdminAccountEntity


class AdminService(ABC):

    @abstractmethod
    async def get_new_reviews(self, last_update: datetime) -> list[ReviewEntity]:
        """
        Used for a poll.

        :param last_update: The last time you received updates
        :return: The list of reviews corresponding to the time interval between `last_update` and current_time
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def login(self, key: str) -> AdminAccountEntity:
        """
        You can use this method to login for the first time. The second authorization will be incorrect.

        :param key: The secret key
        :return: The admin account entity
        :raises InvalidKeyError: The `key` is incorrect or the account has already been registered
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def create_announcement(self, text_content: str | None, preview_photo: str | None) -> AnnouncementEntity:
        """
        :param text_content: The text for an announcement
        :param preview_photo: The address of the photo for an announcement
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
        :raises AnnouncementNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def delete_announcement(self, announcement_id: int):
        """
        :param announcement_id:
        :raises AnnouncementNotFoundError:
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
        :raises AnnouncementNotFoundError:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass
