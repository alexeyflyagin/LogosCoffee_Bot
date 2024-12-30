from datetime import datetime

from sqlalchemy import select, Select, and_, ColumnElement, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.data.logoscoffee.dao.units import set_with_for_update_if
from src.data.logoscoffee.db.models import OrderOrm, ProductAndOrderOrm
from src.data.logoscoffee.entities.enums import OrderState, OrderStateGroup


def __set_options_if(query: Select[tuple[OrderOrm]], is_true: bool) -> Select[tuple[OrderOrm]]:
    if not is_true:
        return query
    return (query.options(joinedload(OrderOrm.product_and_orders)
                          .joinedload(ProductAndOrderOrm.product)))


def __get_criteria_by_state(state: OrderState) -> ColumnElement[bool]:
    match state:
        case OrderState.READY:
            return and_(OrderOrm.date_canceled.is_not(None),
                        OrderOrm.date_ready.is_not(None),
                        OrderOrm.date_completed.is_(None))
        case OrderState.COOKING:
            return and_(OrderOrm.date_canceled.is_not(None),
                        OrderOrm.date_cooking.is_not(None),
                        OrderOrm.date_ready.is_(None))
        case OrderState.PENDING:
            return and_(OrderOrm.date_canceled.is_not(None),
                        OrderOrm.date_pending.is_not(None),
                        OrderOrm.date_cooking.is_(None))
        case OrderState.CANCELED:
            return and_(OrderOrm.date_canceled.is_not(None))
        case OrderState.COMPLETED:
            return and_(OrderOrm.date_completed.is_not(None))
        case OrderState.CREATED:
            return and_(OrderOrm.date_pending.is_(None))


def __set_state_filter(
        query: Select[tuple[OrderOrm]],
        state: OrderState) -> Select[tuple[OrderOrm]]:
    return query.filter(__get_criteria_by_state(state))


def __set_state_group_filter(
        query: Select[tuple[OrderOrm]],
        state_group: OrderStateGroup
) -> Select[tuple[OrderOrm]]:
    match state_group:
        case OrderStateGroup.DRAFT:
            return query.filter(__get_criteria_by_state(OrderState.CREATED))
        case OrderStateGroup.IN_PROGRESS:
            return query.filter(or_(
                __get_criteria_by_state(OrderState.PENDING),
                __get_criteria_by_state(OrderState.COOKING),
                __get_criteria_by_state(OrderState.READY),
            ))
        case OrderStateGroup.CLOSED:
            return query.filter(or_(
                __get_criteria_by_state(OrderState.COMPLETED),
                __get_criteria_by_state(OrderState.CANCELED),
            ))


async def get_by_id(
        s: AsyncSession,
        _id: int,
        join: bool = False,
        with_for_update: bool = False
) -> OrderOrm | None:
    query = select(OrderOrm).filter(OrderOrm.id == _id)
    query = set_with_for_update_if(query, with_for_update)
    query = __set_options_if(query, join)
    res = await s.execute(query)
    return res.unique().scalar_one_or_none()


async def get_by_client_id_and_state(
        s: AsyncSession,
        client_id: int,
        state: OrderState,
        join: bool = False,
        wait_for_update: bool = False
) -> tuple[OrderOrm, ...]:
    query = select(OrderOrm).filter(OrderOrm.client_id == client_id)
    query = __set_state_filter(query, state)
    query = set_with_for_update_if(query, wait_for_update)
    query = __set_options_if(query, join)
    res = await s.execute(query)
    return tuple(res.unique().scalars().all())


async def get_one_by_client_id_and_state(
        s: AsyncSession,
        client_id: int,
        state: OrderState,
        join: bool = False,
        wait_for_update: bool = False
) -> OrderOrm | None:
    query = select(OrderOrm).filter(OrderOrm.client_id == client_id)
    query = __set_state_filter(query, state)
    query = set_with_for_update_if(query, wait_for_update)
    query = __set_options_if(query, join)
    res = await s.execute(query)
    return res.unique().scalar_one_or_none()


async def get_by_client_id_and_state_group(
        s: AsyncSession,
        client_id: int,
        state_group: OrderStateGroup,
        join: bool = False,
        wait_for_update: bool = False
) -> tuple[OrderOrm, ...]:
    query = select(OrderOrm).filter(OrderOrm.client_id == client_id)
    query = __set_state_group_filter(query, state_group)
    query = set_with_for_update_if(query, wait_for_update)
    query = __set_options_if(query, join)
    res = await s.execute(query)
    return tuple(res.unique().scalars().all())


async def get_since_by_date_pending(
        s: AsyncSession,
        date: datetime,
        join: bool = False,
        wait_for_update: bool = False
) -> tuple[OrderOrm, ...]:
    query = select(OrderOrm).filter(OrderOrm.date_pending >= date)
    query = set_with_for_update_if(query, wait_for_update)
    query = __set_options_if(query, join)
    res = await s.execute(query)
    return tuple(res.unique().scalars().all())
