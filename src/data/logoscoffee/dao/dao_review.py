from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.utils import set_with_for_update_if
from src.data.logoscoffee.db.models import ReviewOrm


async def get_by_id(
        s: AsyncSession,
        _id: int,
        with_for_update: bool = False
) -> ReviewOrm | None:
    query = select(ReviewOrm).filter(ReviewOrm.id == _id)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def get_created_since(
        s: AsyncSession,
        date: datetime,
        with_for_update: bool = False
) -> tuple[ReviewOrm, ...]:
    query = select(ReviewOrm).filter(ReviewOrm.date_create >= date)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return tuple(res.scalars().all())
