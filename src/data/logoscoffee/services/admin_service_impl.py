from loguru import logger

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_review, dao_announcement
from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity, AdminAccountEntity
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.interfaces.admin_service import AdminService, ReviewEntity
from src.data.logoscoffee.db.models import *
from src.data.logoscoffee.services.utils import raise_exception_if_none, get_admin_account_by_token
from src.data.logoscoffee.session_manager import SessionManager


class AdminServiceImpl(AdminService):
    COOLDOWN_DISTRIBUTE_ANNOUNCEMENT = timedelta(minutes=10)

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    @staticmethod
    async def __delete_all_announcement(s: AsyncSession):
        announcements = await dao_announcement.get_all(s, with_for_update=True)
        for i in announcements:
            await s.delete(i)
        await s.flush()

    @staticmethod
    async def __safe_get_announcement(s: AsyncSession, announcement_id) -> AnnouncementOrm:
        announcement = await dao_announcement.get_by_id(s, announcement_id)
        raise_exception_if_none(announcement, e=AnnouncementNotFoundError(id=announcement_id))
        return announcement

    def __can_distribute_or_create_announcement(self, account: AdminAccountOrm):
        if account.date_last_announcement_distributing:
            delta_time = datetime.now() - account.date_last_announcement_distributing
            if delta_time < self.COOLDOWN_DISTRIBUTE_ANNOUNCEMENT:
                raise CooldownError(delta_time)

    async def get_new_reviews(
            self,
            token: str,
            last_update: datetime
    ) -> list[ReviewEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                await get_admin_account_by_token(s, token)
                reviews = await dao_review.get_created_since(s, last_update)
                entities = [ReviewEntity.model_validate(i) for i in reviews]
                return entities
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def authorization(
            self,
            token: str
    ) -> AdminAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_admin_account_by_token(s, token)
                entity = AdminAccountEntity.model_validate(account)
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

    async def can_create_or_distribute_announcement(self, token: str) -> bool:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_admin_account_by_token(s, token)
                try:
                    self.__can_distribute_or_create_announcement(account)
                except CooldownError:
                    return False
                return True
        except InvalidTokenError as e:
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
            token: str,
            text_content: str | None,
            preview_photo_data: str | None
    ) -> AnnouncementEntity:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_admin_account_by_token(s, token)
                self.__can_distribute_or_create_announcement(account)
                await self.__delete_all_announcement(s)
                created_announcement = AnnouncementOrm(text_content=text_content, preview_photo_data=preview_photo_data)
                s.add(created_announcement)
                await s.flush()
                res = AnnouncementEntity.model_validate(created_announcement)
                await s.commit()
                logger.success(f"Created announcement (id={res.id})")
                return res
        except (InvalidTokenError, CooldownError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_announcement_by_id(
            self,
            token: str,
            announcement_id: int
    ) -> AnnouncementEntity:
        try:
            async with self.__session_manager.get_session() as s:
                await get_admin_account_by_token(s, token)
                announcement = await self.__safe_get_announcement(s, announcement_id)
                announcement_entity = AnnouncementEntity.model_validate(announcement)
                return announcement_entity
        except (InvalidTokenError, AnnouncementNotFoundError) as e:
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
            token: str,
            announcement_id: int
    ):
        try:
            async with self.__session_manager.get_session() as s:
                await get_admin_account_by_token(s, token)
                announcement = await self.__safe_get_announcement(s, announcement_id)
                await s.delete(announcement)
                await s.commit()
                logger.success(f"Announcement (id={announcement_id}) deleted")
        except (InvalidTokenError, AnnouncementNotFoundError) as e:
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
            token: str,
            announcement_id: int
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_admin_account_by_token(s, token)
                self.__can_distribute_or_create_announcement(account)
                account.date_last_announcement_distributing = datetime.now()
                announcement = await self.__safe_get_announcement(s, announcement_id)
                announcement.date_last_distribute = datetime.now()
                await s.commit()
                logger.success(f"Announcement (id={announcement_id}) distributed")
        except (InvalidTokenError, AnnouncementNotFoundError, CooldownError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
