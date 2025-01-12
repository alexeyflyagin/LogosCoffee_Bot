from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.orm_entities import ClientAccountEntity, AnnouncementEntity


class ClientService(ABC):

    @abstractmethod
    async def get_new_announcements(
            self,
            last_update
    ) -> list[AnnouncementEntity]:
        """
        Used for a poll.

        :param last_update: The last time you received updates

        :return: The list of announcement corresponding to the time interval between `last_update` and current_time

        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def authorization(
            self,
            phone_number: str
    ) -> ClientAccountEntity:
        """
        Each time, it creates a new token for the account.

        :param phone_number:

        :return: The client account entity by `phone_number`

        :raises InvalidPhoneNumberError: If the `phone_number` is incorrect
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def can_submit_review(
            self,
            token: str
    ) -> bool:
        """
        Used to check the limit: whether the client can submit a review.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account

        :return: `True` if the limit is not reached, or `False`

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def submit_review(
            self,
            token: str,
            text: str
    ):
        """
        Anonymously submits a review.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the client account
        :param text: The text for a review

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises CooldownError: If a review has already been submitted recently
        :raises EmptyTextError: If `text` is empty
        :raises DatabaseError:
        :raises UnknownError:
        """
