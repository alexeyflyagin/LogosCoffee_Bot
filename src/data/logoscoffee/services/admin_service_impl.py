from loguru import logger

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_review, dao_announcement, dao_admin_account
from src.data.logoscoffee.dao.units import raise_exception_if_none
from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity, AdminAccountEntity
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.interfaces.admin_service import AdminService, ReviewEntity
from src.data.logoscoffee.db.models import *
from src.data.logoscoffee.session_manager import SessionManager


class AdminServiceImpl(AdminService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __safe_get_announcement(self, s: AsyncSession, announcement_id) -> AnnouncementOrm:
        announcement = await dao_announcement.get_by_id(s, announcement_id)
        raise_exception_if_none(announcement, e=AnnouncementNotFoundError(id=announcement_id))
        return announcement

    def __can_publish_announcement(self, account: AdminAccountOrm):
        if account.date_last_announcement_distributing:
            delta_time = datetime.now() - account.date_last_announcement_distributing
            if delta_time < timedelta(minutes=10):
                raise CooldownError(delta_time)

    async def get_new_reviews(
            self,
            last_update: datetime
    ) -> list[ReviewEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                reviews = await dao_review.get_created_since(s, last_update)
                entities = [ReviewEntity.model_validate(i) for i in reviews]
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def login(
            self,
            key: str
    ) -> AdminAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                account = await dao_admin_account.get_by_key(s, key)
                if account is None or account.date_authorized:
                    raise InvalidKeyError(key)
                account.date_authorized = datetime.now()
                await s.flush()
                entity = AdminAccountEntity.model_validate(account)
                await s.commit()
                return entity
        except InvalidKeyError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def create_announcement(
            self,
            text_content: str | None,
            preview_photo: str | None
    ) -> AnnouncementEntity:
        try:
            async with self.__session_manager.get_session() as s:
                created_announcement = AnnouncementOrm(text_content=text_content, preview_photo=preview_photo)
                s.add(created_announcement)
                await s.flush()
                res = AnnouncementEntity.model_validate(created_announcement)
                await s.commit()
                return res
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_announcement_by_id(
            self,
            announcement_id: int
    ) -> AnnouncementEntity:
        try:
            async with self.__session_manager.get_session() as s:
                announcement = await self.__safe_get_announcement(s, announcement_id)
                announcement_entity = AnnouncementEntity.model_validate(announcement)
                return announcement_entity
        except AnnouncementNotFoundError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def delete_announcement(
            self,
            announcement_id: int
    ):
        try:
            async with self.__session_manager.get_session() as s:
                announcement = await self.__safe_get_announcement(s, announcement_id)
                await s.delete(announcement)
                await s.commit()
        except AnnouncementNotFoundError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def distribute_announcement(
            self,
            account_id: int,
            announcement_id: int
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await dao_admin_account.get_by_id(s, account_id, with_for_update=True)
                self.__can_publish_announcement(account)
                account.date_last_announcement_distributing = datetime.now()
                announcement = await self.__safe_get_announcement(s, announcement_id)
                announcement.date_last_distribute = datetime.now()
                await s.commit()
        except (AnnouncementNotFoundError, CooldownError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
