import string
import random

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_client_account
from src.data.logoscoffee.db.models import ClientAccountOrm
from src.data.logoscoffee.exceptions import InvalidTokenError, TokenGenerateError

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"


def raise_exception_if_none(it, e):
    if e is not None and it is None:
        raise e


async def get_client_account_by_token(s: AsyncSession, token: str) -> ClientAccountOrm:
    account = await dao_client_account.get_by_token(s, token, with_for_update=True)
    raise_exception_if_none(account, e=InvalidTokenError(token=token))
    return account


async def generate_token(s: AsyncSession) -> str:
    try:
        for i in range(300):
            new_token = ''.join(random.choices(TOKEN_SYMBOLS, k=16))
            account = await dao_client_account.get_by_token(s, new_token)
            if not account:
                return new_token
        raise TokenGenerateError()
    except TokenGenerateError as e:
        logger.critical(e)
        raise
