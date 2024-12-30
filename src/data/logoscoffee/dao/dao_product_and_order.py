from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.data.logoscoffee.dao.units import set_with_for_update_if
from src.data.logoscoffee.db.models import ProductAndOrderOrm


def __set_options_if(query: Select[tuple[ProductAndOrderOrm]], is_true: bool) -> Select[tuple[ProductAndOrderOrm]]:
    if not is_true:
        return query
    return (query
            .options(joinedload(ProductAndOrderOrm.product))
            .options(joinedload(ProductAndOrderOrm.order)))


async def get(
        s: AsyncSession,
        product_id: int,
        order_id: int,
        join: bool = False,
        with_for_update: bool = False
) -> tuple[ProductAndOrderOrm, ...]:
    query = (select(ProductAndOrderOrm)
             .filter(ProductAndOrderOrm.order_id == order_id)
             .filter(ProductAndOrderOrm.product_id == product_id))
    query = __set_options_if(query, join)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return tuple(res.unique().scalars().all())


async def get_by_order_id(
        s: AsyncSession,
        order_id: int,
        join: bool = False,
        with_for_update: bool = False
) -> tuple[ProductAndOrderOrm, ...]:
    query = (select(ProductAndOrderOrm)
             .filter(ProductAndOrderOrm.order_id == order_id))
    query = __set_options_if(query, join)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return tuple(res.unique().scalars().all())
