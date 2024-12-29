from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.units import set_wait_for_update_if
from src.data.logoscoffee.db.models import ReviewOrm


async def get_by_id(s: AsyncSession, _id: int, wait_for_update=False) -> ReviewOrm:
    query = select(ReviewOrm).filter(ReviewOrm.id == _id)
    set_wait_for_update_if(query, wait_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()

async def get_created_since(s: AsyncSession, date: datetime, wait_for_update=False) -> tuple[ReviewOrm, ...]:
    query = select(ReviewOrm).filter(ReviewOrm.date_create >= date)
    set_wait_for_update_if(query, wait_for_update)
    res = await s.execute(query)
    return tuple(res.scalars().all())
