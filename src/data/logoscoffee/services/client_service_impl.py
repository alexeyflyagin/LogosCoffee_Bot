import string

from loguru import logger
from pydantic import TypeAdapter
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.checks import check_text_is_not_empty
from src.data.logoscoffee.dao import dao_announcement, dao_product, dao_client_account
from src.data.logoscoffee.entities.general_entities import MenuEntity
from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity, ClientAccountEntity, ProductEntity
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.db.models import ClientAccountOrm, ReviewOrm
from src.data.logoscoffee.services.units import create_draft_orm
from src.data.logoscoffee.session_manager import SessionManager

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"


class ClientServiceImpl(ClientService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __can_make_review(self, account: ClientAccountOrm):
        pass
        if account.date_last_review is not None:
            delta_time = datetime.now() - account.date_last_review
            if delta_time < timedelta(hours=1):
                raise CooldownError(delta_time)

    async def get_new_announcements(
            self,
            last_update
    ) -> list[AnnouncementEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                announcements = await dao_announcement.get_since_by_last_distribute(s, last_update)
                entities = [AnnouncementEntity.model_validate(i) for i in announcements]
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


    async def login(
            self,
            phone_number: str
    ) -> ClientAccountEntity:
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
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def can_submit_review(
            self,
            account_id: int
    ) -> bool:
        try:
            async with self.__session_manager.get_session() as s:
                account = await dao_client_account.get_by_id(s, account_id)
                await self.__can_make_review(account)
                return True
        except CooldownError:
            return False
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


    async def submit_review(
            self,
            account_id: int,
            text: str
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await dao_client_account.get_by_id(s, account_id, with_for_update=True)
                await self.__can_make_review(account)
                current_time = datetime.now()
                account.date_last_review = current_time
                check_text_is_not_empty(text)
                new_comment = ReviewOrm(date_create=current_time, text_content=text)
                s.add(new_comment)
                await s.commit()
        except (EmptyTextError, CooldownError) as e:
            logger.warning(e)
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
                products = await dao_product.get_by_is_available(s, is_available=True)
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

    async def get_product_by_id(
            self,
            product_id: int
    ) -> ProductEntity:
        try:
            async with self.__session_manager.get_session() as s:
                product = await dao_product.get_by_id(s, product_id)
                if product is None:
                    raise ProductNotFoundError(id=product_id)
                entity = ProductEntity.model_validate(product)
                return entity
        except ProductNotFoundError as e:
            logger.warning(e)
            raise UnknownError(e)
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


