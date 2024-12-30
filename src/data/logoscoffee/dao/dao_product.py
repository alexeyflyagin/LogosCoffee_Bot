from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.units import set_with_for_update_if
from src.data.logoscoffee.db.models import ProductOrm


async def get_by_id(
        s: AsyncSession, _id: int,
        wait_for_update: bool = False
) -> ProductOrm | None:
    query = select(ProductOrm).filter(ProductOrm.id == _id)
    query = set_with_for_update_if(query, wait_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def get_by_is_available(
        s: AsyncSession,
        is_available: bool,
        with_for_update: bool = False
) -> tuple[ProductOrm, ...]:
    query = select(ProductOrm).filter(ProductOrm.is_available == is_available)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return tuple(res.scalars().all())
