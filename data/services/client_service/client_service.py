import random
import string

from asyncpg.pgproto.pgproto import timedelta
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typeguard import typechecked

from data.services.checks import check_text_is_not_empty
from data.services.client_service.entities import ClientAuthorizationData
from data.services.database import database
from data.services.exceptions import *
from data.services.models import ClientAccountOrm, ReviewOrm

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"

@typechecked
async def __generate_token(s: AsyncSession) -> str:
    try:
        for i in range(300):
            new_token = ''.join(random.choices(TOKEN_SYMBOLS, k=8))
            query = await s.execute(select(ClientAccountOrm).filter(ClientAccountOrm.token == new_token))
            if not query.scalars().first(): return new_token
        raise TokenGenerateError()
    except TokenGenerateError as e:
        logger.critical(e)
        raise

@typechecked
async def __validate_token(s: AsyncSession, token: str | None) -> ClientAccountOrm:
    if token is None:
        raise InvalidToken(token)
    res = await s.execute(select(ClientAccountOrm).filter(ClientAccountOrm.token == token).with_for_update())
    res = res.scalars().first()
    if res is None:
        raise InvalidToken(token)
    return res


@typechecked
async def __can_make_review(s: AsyncSession, account: ClientAccountOrm):
    if account.date_last_review is not None:
        delta_time = datetime.now() - account.date_last_review
        if delta_time < timedelta(days=1):
            raise CooldownError(delta_time)


@typechecked
async def validate_token(token: str | None):
    try:
        async with database.session_factory() as s:
            await __validate_token(s, token)
    except InvalidToken as e:
        logger.warning(e)
        raise
    except SQLAlchemyError as e:
        logger.error(e)
        raise DatabaseError(e)
    except Exception as e:
        logger.exception(e)
        raise UnknownError(e)



@typechecked
async def log_in(phone_number: str) -> ClientAuthorizationData:
    try:
        async with database.session_factory() as s:
            token = await __generate_token(s)
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


@typechecked
async def can_make_review(token: str):
    try:
        async with database.session_factory() as s:
            account = await __validate_token(s, token)
            await __can_make_review(s, account)
    except (InvalidToken, CooldownError) as e:
        logger.warning(e)
        raise
    except SQLAlchemyError as e:
        logger.error(e)
        raise DatabaseError(e)
    except Exception as e:
        logger.exception(e)
        raise UnknownError(e)


@typechecked
async def make_review(token: str, text: str):
    try:
        async with database.session_factory() as s:
            account = await __validate_token(s, token)
            await __can_make_review(s, account)
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


