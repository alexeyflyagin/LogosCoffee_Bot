import random
import string

from asyncpg.pgproto.pgproto import timedelta
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.checks import check_text_is_not_empty
from src.data.logoscoffee.interfaces.client_service import ClientAuthorizationData, ClientService
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.db.models import ClientAccountOrm, ReviewOrm
from src.data.logoscoffee.session_manager import SessionManager

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"


class ClientServiceImpl(ClientService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager


    async def __generate_token(self, s: AsyncSession) -> str:
        try:
            for i in range(300):
                new_token = ''.join(random.choices(TOKEN_SYMBOLS, k=8))
                query = await s.execute(select(ClientAccountOrm).filter(ClientAccountOrm.token == new_token))
                if not query.scalars().first(): return new_token
            raise TokenGenerateError()
        except TokenGenerateError as e:
            logger.critical(e)
            raise

    async def __validate_token(self, s: AsyncSession, token: str | None) -> ClientAccountOrm:
        if token is None:
            raise InvalidToken(token)
        res = await s.execute(select(ClientAccountOrm).filter(ClientAccountOrm.token == token).with_for_update())
        res = res.scalars().first()
        if res is None:
            raise InvalidToken(token)
        return res

    async def __can_make_review(self, account: ClientAccountOrm):
        pass
        # if account.date_last_review is not None:
        #     delta_time = datetime.now() - account.date_last_review
        #     if delta_time < timedelta(hours=1):
        #         raise CooldownError(delta_time)

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

    async def login(self, phone_number: str) -> ClientAuthorizationData:
        try:
            async with self.__session_manager.get_session() as s:
                token = await self.__generate_token(s)
                new_client = ClientAccountOrm(
                    token=token,
                    phone_number=phone_number,
                    date_registration=datetime.now(),
                )
                s.add(new_client)
                await s.commit()
                return ClientAuthorizationData(token=token)
        except (InvalidToken, SQLAlchemyError) as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)

    async def can_make_review(self, token: str | None):
        try:
            async with self.__session_manager.get_session() as s:
                account = await self.__validate_token(s, token)
                await self.__can_make_review(account)
        except (InvalidToken, CooldownError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)


    async def make_review(self, token: str | None, text: str):
        try:
            async with self.__session_manager.get_session() as s:
                account = await self.__validate_token(s, token)
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


