from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.utils import set_with_for_update_if
from src.data.logoscoffee.db.models import MenuOrm


async def get(
        s: AsyncSession,
        with_for_update: bool = False
) -> MenuOrm:
    query = select(MenuOrm).limit(limit=1)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one()
