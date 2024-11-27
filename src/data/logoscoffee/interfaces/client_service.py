from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.general_entities import MenuEntity
from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity, ClientAccountEntity, ProductEntity


class ClientService(ABC):

    @abstractmethod
    async def get_new_announcements(self, last_update) -> list[AnnouncementEntity]:
        """
        Used for a poll.

        :param last_update: The last time you received updates
        :return: The list of announcement corresponding to the time interval between `last_update` and current_time
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def login(self, phone_number: str) -> ClientAccountEntity:
        """
        :param phone_number:
        :return: The client account entity
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def can_submit_review(self, account_id: int) -> bool:
        """
        Used to check the limit: whether the client can submit a review.

        (The user can submit a review once an hour)

        :param account_id:
        :return: `True` if the limit is not reached, or `False`
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def submit_review(self, account_id: int, text: str):
        """
        Anonymously submits a review.

        :param account_id: Uses to check account limits
        :param text: The text for a review
        :raises EmptyTextError: If `text` is empty
        :raises CooldownError: If a review has already been submitted recently
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_menu(self) -> MenuEntity:
        """
        :return: The menu entity object with a list of available products
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> ProductEntity:
        """
        :param product_id:
        :return: The product entity
        :raises ProductNotFound:
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass
