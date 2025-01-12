import string

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.checks import check_text_is_not_empty, check_phone_number
from src.data.logoscoffee.services.utils import get_client_account_by_token, generate_token
from src.data.logoscoffee.dao import dao_announcement, dao_client_account
from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity, ClientAccountEntity
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.db.models import ClientAccountOrm, ReviewOrm
from src.data.logoscoffee.session_manager import SessionManager

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"


class ClientServiceImpl(ClientService):
    COOLDOWN_MAKE_REVIEW = timedelta(hours=1)

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __can_make_review(self, account: ClientAccountOrm):
        if account.date_last_review is None:
            return
        delta_time = datetime.now() - account.date_last_review
        if delta_time < self.COOLDOWN_MAKE_REVIEW:
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

    async def authorization(
            self,
            phone_number: str
    ) -> ClientAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                check_phone_number(phone_number)
                account = await dao_client_account.get_by_phone_number(s, phone_number, with_for_update=True)
                token = await generate_token(s)
                if account is None:
                    account = ClientAccountOrm(phone_number=phone_number, token=token)
                    s.add(account)
                    await s.flush()
                account.token = token
                entity = ClientAccountEntity.model_validate(account)
                await s.commit()
                return entity
        except InvalidPhoneNumberError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def can_submit_review(
            self,
            token: str
    ) -> bool:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                try:
                    await self.__can_make_review(account)
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

    async def submit_review(
            self,
            token: str,
            text: str
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                await self.__can_make_review(account)
                check_text_is_not_empty(text)
                current_time = datetime.now()
                account.date_last_review = current_time
                new_review = ReviewOrm(date_create=current_time, text_content=text)
                s.add(new_review)
                new_review_id = new_review.id
                await s.commit()
                logger.success(f"Review (id={new_review_id}) submitted")
        except (InvalidTokenError, EmptyTextError, CooldownError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
