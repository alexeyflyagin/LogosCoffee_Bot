from abc import ABC, abstractmethod
from datetime import datetime

from src.data.logoscoffee.entities.orm_entities import ReviewEntity, AnnouncementEntity, AdminAccountEntity, MenuEntity


class AdminMenuService(ABC):

    @abstractmethod
    async def update_menu(
            self,
            token: str,
            text_content: str,
    ):
        """
        It changes the menu text.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the admin account
        :param text_content: A content

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def get_menu(self) -> MenuEntity:
        """
        :raises DatabaseError:
        :raises UnknownError:
        """
