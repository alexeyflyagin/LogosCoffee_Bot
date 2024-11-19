import string

from loguru import logger
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.checks import check_text_is_not_empty
from src.data.logoscoffee.entities.general_entities import MenuEntity
from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity, ClientAccountEntity, ProductEntity
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.db.models import ClientAccountOrm, ReviewOrm, AnnouncementOrm, ProductOrm
from src.data.logoscoffee.services.units import create_draft_orm
from src.data.logoscoffee.session_manager import SessionManager

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"


class ClientServiceImpl(ClientService):



    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __can_make_review(self, account: ClientAccountOrm):
        pass
        # if account.date_last_review is not None:
        #     delta_time = datetime.now() - account.date_last_review
        #     if delta_time < timedelta(hours=1):
        #         raise CooldownError(delta_time)

    async def get_new_announcements(self, last_update_time) -> list[AnnouncementEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(AnnouncementOrm).filter(AnnouncementOrm.date_last_distribute >= last_update_time))
                announcements = res.scalars().all()
                entities = [AnnouncementEntity.model_validate(i) for i in announcements]
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


    async def login(self, phone_number: str) -> ClientAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                new_client = ClientAccountOrm(phone_number=phone_number)
                s.add(new_client)
                await s.flush()
                await create_draft_orm(s, client_id=new_client.id)
                entity = ClientAccountEntity.model_validate(new_client)
                await s.commit()
                return entity
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)

    async def can_create_review(self, account_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(ClientAccountOrm).filter(ClientAccountOrm.id == account_id))
                account = res.scalars().first()
                await self.__can_make_review(account)
        except CooldownError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


    async def create_review(self, account_id: int, text: str):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(ClientAccountOrm).filter(ClientAccountOrm.id == account_id).with_for_update())
                account = res.scalars().first()
                await self.__can_make_review(account)
                current_time = datetime.now()
                account.date_last_review = current_time
                check_text_is_not_empty(text)
                new_comment = ReviewOrm(date_create=current_time, text_content=text)
                s.add(new_comment)
                await s.commit()
        except (EmptyTextError, CooldownError) as e:
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

    async def get_menu(self) -> MenuEntity:
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(ProductOrm).filter(ProductOrm.is_available == True))
                products = res.unique().scalars().all()
                type_adapter = TypeAdapter(list[ProductEntity])
                entities = type_adapter.validate_python(products)
                menu_entity = MenuEntity(all_products=entities)
                return menu_entity
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_product_by_id(self, product_id: int) -> ProductEntity:
        pass


