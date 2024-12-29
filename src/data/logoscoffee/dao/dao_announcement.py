from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.units import set_wait_for_update_if
from src.data.logoscoffee.db.models import AnnouncementOrm


async def get_by_id(s: AsyncSession, _id: int, wait_for_update=False) -> AnnouncementOrm:
    query = select(AnnouncementOrm).filter(AnnouncementOrm.id == _id)
    set_wait_for_update_if(query, wait_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()

async def get_since_by_last_distribute(s: AsyncSession, date: datetime, wait_for_update=False) -> tuple[AnnouncementOrm, ...]:
    query = select(AnnouncementOrm).filter(AnnouncementOrm.date_last_distribute >= date)
    set_wait_for_update_if(query, wait_for_update)
    res = await s.execute(query)
    return tuple(res.scalars().all())
