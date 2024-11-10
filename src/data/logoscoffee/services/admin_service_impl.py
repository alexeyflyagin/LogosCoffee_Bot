from loguru import logger

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.entities.admin_entities import ReviewEntity
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.interfaces.admin_service import AdminService
from src.data.logoscoffee.db.models import *
from src.data.logoscoffee.session_manager import SessionManager


class AdminServiceImpl(AdminService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager


    async def get_new_reviews(self, last_update: datetime) -> list[ReviewEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(ReviewOrm).filter(ReviewOrm.date_create >= last_update))
                reviews = res.scalars().all()
                entities = [ReviewEntity.model_validate(i) for i in reviews]
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


    async def login(self, token: str | None):
        try:
            async with self.__session_manager.get_session() as s:
                query = await s.execute(select(AdminAccountOrm).filter(AdminAccountOrm.token == token))
                account = query.scalars().first()
                if account is None:
                    raise InvalidToken(token)
        except InvalidToken as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


