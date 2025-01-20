from aiohttp.payload import Order
from sqlalchemy import select, ColumnElement, and_, Select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.utils import set_with_for_update_if
from src.data.logoscoffee.db.models import OrderOrm
from src.data.logoscoffee.enums import OrderState, OrderStateGroup


def __get_criteria_by_state(state: OrderState) -> ColumnElement[bool]:
    match state:
        case OrderState.PENDING:
            return and_(OrderOrm.date_pending.is_not(None),
                        OrderOrm.date_canceled.is_(None),
                        OrderOrm.date_cooking.is_(None))
        case OrderState.COOKING:
            return and_(OrderOrm.date_cooking.is_not(None),
                        OrderOrm.date_canceled.is_(None),
                        OrderOrm.date_ready.is_(None))
        case OrderState.READY:
            return and_(OrderOrm.date_ready.is_not(None),
                        OrderOrm.date_canceled.is_(None),
                        OrderOrm.date_completed.is_(None))
        case OrderState.CANCELED:
            return and_(OrderOrm.date_canceled.is_not(None))
        case OrderState.COMPLETED:
            return and_(OrderOrm.date_completed.is_not(None))

def __set_state_filter(
        query: Select[tuple[OrderOrm]],
        state: OrderState
) -> Select[tuple[OrderOrm]]:
    return query.filter(__get_criteria_by_state(state))


def __set_state_group_filter(
        query: Select[tuple[OrderOrm]],
        state_group: OrderStateGroup
) -> Select[tuple[OrderOrm]]:
    match state_group:
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


async def get_active_order_by_client_id(
        s: AsyncSession,
        client_id: int,
        with_for_update: bool = False
) -> OrderOrm:
    query = select(OrderOrm).filter(OrderOrm.client_id == client_id)
    query = __set_state_group_filter(query, OrderStateGroup.IN_PROGRESS)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()
