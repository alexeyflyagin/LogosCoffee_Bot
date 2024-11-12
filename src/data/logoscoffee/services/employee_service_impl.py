from loguru import logger

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity
from src.data.logoscoffee.interfaces.employee_service import EmployeeService
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.db.models import EmployeeAccountOrm
from src.data.logoscoffee.session_manager import SessionManager


class EmployeeServiceImpl(EmployeeService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def login(self, key: str | None) -> EmployeeAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                query = await s.execute(select(EmployeeAccountOrm).filter(EmployeeAccountOrm.key == key))
                account = query.scalars().first()
                if account is None:
                    raise InvalidKey(key)
                return EmployeeAccountEntity.model_validate(account)
        except InvalidKey as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
