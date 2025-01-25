from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity


class EmployeeService(ABC):

    @abstractmethod
    async def authorization(
            self,
            token: str
    ) -> EmployeeAccountEntity:
        """
        You can use this method to authorization.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the employee account

        :return: The employee account entity

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """

    @abstractmethod
    async def validate_token(
            self,
            token: str
    ):
        """
        Use it to verify the validity of the token.

        :param token: A unique 16-digit line (A-Z|a-z|0-9) associated with the employee account

        :raises InvalidTokenError: If the `token` is specified incorrectly or is missing
        :raises DatabaseError:
        :raises UnknownError:
        """
