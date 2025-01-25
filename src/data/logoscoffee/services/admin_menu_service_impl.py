from datetime import datetime

from src.loggers import service_logger as logger
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.dao import dao_menu
from src.data.logoscoffee.entities.orm_entities import MenuEntity
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError, InvalidTokenError
from src.data.logoscoffee.interfaces.admin_menu_service import AdminMenuService
from src.data.logoscoffee.services.utils import get_admin_account_by_token
from src.data.logoscoffee.session_manager import SessionManager


class AdminMenuServiceImpl(AdminMenuService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def update_menu(self, token: str, text_content: str):
        try:
            async with self.__session_manager.get_session() as s:
                await get_admin_account_by_token(s, token)
                menu = await dao_menu.get(s, with_for_update=True)
                menu.text_content = text_content
                menu.last_date_update = datetime.now()
                await s.commit()
        except InvalidTokenError as e:
            logger.debug(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_menu(self) -> MenuEntity:
        try:
            async with self.__session_manager.get_session() as s:
                menu = await dao_menu.get(s)
                entity = MenuEntity.model_validate(menu)
                return entity
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
