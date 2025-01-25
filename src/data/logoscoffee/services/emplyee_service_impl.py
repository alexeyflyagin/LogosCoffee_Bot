from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.interfaces.employee_service import EmployeeService
from src.data.logoscoffee.services.utils import get_employee_account_by_token
from src.data.logoscoffee.session_manager import SessionManager


class EmployeeServiceImpl(EmployeeService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def authorization(
            self,
            token: str
    ) -> EmployeeAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_employee_account_by_token(s, token)
                entity = EmployeeAccountEntity.model_validate(account)
                await s.commit()
                return entity
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def validate_token(self, token: str):
        try:
            async with self.__session_manager.get_session() as s:
                await get_employee_account_by_token(s, token)
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
