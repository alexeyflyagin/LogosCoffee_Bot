from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import ReviewEntity, AnnouncementEntity, AdminAccountEntity


class AdminService(ABC):

    @abstractmethod
    async def get_new_reviews(
            self,
            token: str,
            last_update: datetime
    ) -> list[ReviewEntity]:
        """
        Used for a poll.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account
        :param last_update: The last time you received updates

        :return: The list of reviews corresponding to the time interval between `last_update` and current_time

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def authorization(
            self,
            token: str
    ) -> AdminAccountEntity:
        """
        You can use this method to authorization.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account

        :return: The admin account entity

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def can_create_or_distribute_announcement(
            self,
            token: str,
    ) -> bool:
        """

        Used to check the limit: whether the admin can create or distribute a review.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account

        :return: `True` if the limit is not reached, or `False`

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def create_announcement(
            self,
            token: str,
            text_content: str | None,
            preview_photo_data: str | None
    ) -> AnnouncementEntity:
        """
        Create an announcement.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account
        :param text_content: The text for the new announcement
        :param preview_photo_data: The preview photo data for the new announcement

        :return: The created announcement entity

        :raises CooldownError: If an announcement has already been created or distributed recently
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def get_announcement_by_id(
            self,
            token: str,
            announcement_id: int
    ) -> AnnouncementEntity:
        """
        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account
        :param announcement_id:

        :return: The announcement entity

        :raises AnnouncementNotFoundError:
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def delete_announcement(
            self,
            token: str,
            announcement_id: int
    ):
        """
        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account
        :param announcement_id:

        :raises AnnouncementNotFoundError:
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def distribute_announcement(
            self,
            token: str,
            announcement_id: int
    ):
        """
        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account
        :param announcement_id:

        :raises AnnouncementNotFoundError:
        :raises CooldownError: If an announcement has already been created or distributed recently
        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
