import string
import random

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_client_account, dao_order, dao_product
from src.data.logoscoffee.dao.units import raise_exception_if_none
from src.data.logoscoffee.db.models import OrderOrm, ClientAccountOrm
from src.data.logoscoffee.entities.enums import OrderState
from src.data.logoscoffee.exceptions import InvalidTokenError, ProductNotFoundError, TokenGenerateError

TOKEN_SYMBOLS = string.ascii_letters + string.digits + "-_"


async def get_draft_order_by_client_id(s, client_id: int, join: bool = False):
    draft_order = await dao_order.get_one_by_client_id_and_state(s, client_id, OrderState.CREATED, join=join)
    return draft_order


async def get_client_account_by_token(s: AsyncSession, token: str) -> ClientAccountOrm:
    account = await dao_client_account.get_by_token(s, token, with_for_update=True)
    raise_exception_if_none(account, e=InvalidTokenError(token=token))
    return account


async def safe_get_product_by_id(s: AsyncSession, product_id: int) -> ClientAccountOrm:
    product = await dao_product.get_by_id(s, product_id)
    raise_exception_if_none(product, e=ProductNotFoundError(id=product_id))
    return product


async def create_draft_orm(s: AsyncSession, client_id: int) -> OrderOrm:
    order_orm = OrderOrm(client_id=client_id)
    s.add(order_orm)
    await s.flush()
    return order_orm


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
