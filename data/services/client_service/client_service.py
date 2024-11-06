import random
import string
from random import choices

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typeguard import typechecked

from data.services import utils
from data.services.client_service.entities import ClientAuthorizationData
from data.services.database import database
from data.services.exceptions import *
from data.services.models import ClientAccountOrm


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
async def log_in(phone_number: str) -> ClientAuthorizationData:
    try:
        async with database.session_factory() as s:
            token = await __generate_token(s)
            new_client = ClientAccountOrm(
                token=token,
                phone_number=phone_number,
                date_registration=utils.get_current_timestamp(),
            )
            s.add(new_client)
            await s.commit()
            return ClientAuthorizationData(token=token)
    except SQLAlchemyError as e:
        await s.rollback()
        logger.error(e)
        raise DatabaseError(e)
    except Exception as e:
        await s.rollback()
        logger.exception(e)
        raise UnknownError(e)