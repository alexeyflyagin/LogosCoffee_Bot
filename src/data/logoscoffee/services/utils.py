import random
import string

from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_client_account, dao_admin_account, dao_employee_account, dao_order
from src.data.logoscoffee.db.models import ClientAccountOrm, AdminAccountOrm, EmployeeAccountOrm
from src.data.logoscoffee.exceptions import InvalidTokenError, TokenGenerateError, PickupCodeGenerateError
from src.loggers import service_logger as logger

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"


def raise_exception_if_none(it, e):
    if e is not None and it is None:
        raise e


async def get_client_account_by_token(s: AsyncSession, token: str) -> ClientAccountOrm:
    account = await dao_client_account.get_by_token(s, token, with_for_update=True)
    raise_exception_if_none(account, e=InvalidTokenError(token=token))
    return account


async def get_admin_account_by_token(s: AsyncSession, token: str) -> AdminAccountOrm:
    account = await dao_admin_account.get_by_token(s, token, with_for_update=True)
    raise_exception_if_none(account, e=InvalidTokenError(token=token))
    return account


async def get_employee_account_by_token(s: AsyncSession, token: str) -> EmployeeAccountOrm:
    account = await dao_employee_account.get_by_token(s, token, with_for_update=True)
    raise_exception_if_none(account, e=InvalidTokenError(token=token))
    return account


async def generate_pickup_code(s: AsyncSession) -> str:
    try:
        pickup_code_length = 6
        for i in range(600):
            new_pickup_code = ''.join(random.choices(string.digits, k=pickup_code_length))
            if new_pickup_code == '0' * pickup_code_length:
                continue
            order = await dao_order.get_by_pickup_code(s, new_pickup_code)
            if not order:
                return new_pickup_code
        raise PickupCodeGenerateError()
    except PickupCodeGenerateError as e:
        logger.critical(e)
        raise


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
