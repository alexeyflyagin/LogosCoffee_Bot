from loguru import logger

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee import checks
from src.data.logoscoffee.entities.orm_entities import PromotionalOfferEntity
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.interfaces.admin_service import AdminService, ReviewEntity
from src.data.logoscoffee.db.models import *
from src.data.logoscoffee.session_manager import SessionManager


class AdminServiceImpl(AdminService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __get_promotional_offer(self, s: AsyncSession, offer_id) -> PromotionalOfferOrm:
        res = await s.execute(select(PromotionalOfferOrm).filter(PromotionalOfferOrm.id == offer_id))
        offer = res.scalars().first()
        if offer is None:
            raise PromotionalOfferDoesNotExist(id=offer_id)
        return offer

    async def __validate_token(self, s: AsyncSession, token: str | None) -> AdminAccountOrm:
        if token is None:
            raise InvalidToken(token)
        res = await s.execute(select(AdminAccountOrm).filter(AdminAccountOrm.token == token).with_for_update())
        res = res.scalars().first()
        if res is None:
            raise InvalidToken(token)
        return res

    async def validate_token(self, token: str | None):
        try:
            async with self.__session_manager.get_session() as s:
                await self.__validate_token(s, token)
        except InvalidToken as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

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

    async def make_promotional_offer(self, token: str | None, text_content: str | None, promotional_photo_url: str | None) -> PromotionalOfferEntity:
        try:
            async with self.__session_manager.get_session() as s:
                await self.__validate_token(s, token)
                offer = PromotionalOfferOrm(date_create=datetime.now(), text_content=text_content, preview_photo_url=promotional_photo_url)
                s.add(offer)
                await s.flush()
                res = PromotionalOfferEntity.model_validate(offer)
                await s.commit()
                return res
        except InvalidToken as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)

    async def get_promotional_offer(self, token: str | None, offer_id: int) -> PromotionalOfferEntity:
        try:
            async with self.__session_manager.get_session() as s:
                await self.__validate_token(s, token)
                offer = await self.__get_promotional_offer(s, offer_id)
                offer_entity = PromotionalOfferEntity.model_validate(offer)
                return offer_entity
        except (PromotionalOfferDoesNotExist, InvalidToken) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def delete_promotional_offer(self, token: str | None, offer_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                await self.__validate_token(s, token)
                offer = await self.__get_promotional_offer(s, offer_id)
                await s.delete(offer)
                await s.commit()
        except (PromotionalOfferDoesNotExist, InvalidToken) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


    async def start_promotional_offer(self, token: str | None, offer_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                await self.__validate_token(s, token)
                offer = await self.__get_promotional_offer(s, offer_id)
                offer.date_start = datetime.now()
                await s.commit()
        except (PromotionalOfferDoesNotExist, InvalidToken) as e:
            await s.rollback()
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)




