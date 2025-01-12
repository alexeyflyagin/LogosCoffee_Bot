from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.utils import set_with_for_update_if
from src.data.logoscoffee.db.models import ClientAccountOrm


async def get_by_id(
        s: AsyncSession,
        _id: int,
        with_for_update: bool = False
) -> ClientAccountOrm | None:
    query = select(ClientAccountOrm).filter(ClientAccountOrm.id == _id)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def get_by_token(
        s: AsyncSession,
        token: str,
        with_for_update: bool = False
) -> ClientAccountOrm | None:
    query = select(ClientAccountOrm).filter(ClientAccountOrm.token == token)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def get_by_phone_number(
        s: AsyncSession,
        phone_number: str,
        with_for_update: bool = False
) -> ClientAccountOrm | None:
    query = select(ClientAccountOrm).filter(ClientAccountOrm.phone_number == phone_number)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()
