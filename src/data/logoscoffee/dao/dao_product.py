from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.units import set_wait_for_update_if
from src.data.logoscoffee.db.models import ProductOrm


async def get_by_id(s: AsyncSession, _id: int, wait_for_update=False) -> ProductOrm:
    query = select(ProductOrm).filter(ProductOrm.id == _id)
    set_wait_for_update_if(query, wait_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()

async def get_by_is_available(s: AsyncSession, is_available: bool, wait_for_update=False) -> tuple[ProductOrm, ...]:
    query = select(ProductOrm).filter(ProductOrm.is_available == is_available)
    set_wait_for_update_if(query, wait_for_update)
    res = await s.execute(query)
    return tuple(res.scalars().all())
