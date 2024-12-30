from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.units import set_with_for_update_if
from src.data.logoscoffee.db.models import EventSubscriberOrm


async def get(
        s: AsyncSession,
        event_name: str,
        chat_id: int,
        with_for_update: bool = False
) -> EventSubscriberOrm | None:
    query = (select(EventSubscriberOrm)
             .filter(EventSubscriberOrm.event_name == event_name)
             .filter(EventSubscriberOrm.chat_id == chat_id))
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def get_by_event_name(
        s: AsyncSession,
        event_name: str,
        with_for_update: bool = False
) -> tuple[EventSubscriberOrm, ...]:
    query = select(EventSubscriberOrm).filter(EventSubscriberOrm.event_name == event_name)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return tuple(res.scalars().all())
