from html import escape

from aiogram import Bot
from aiogram.types import Message

from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.enums import OrderState, OrderStateGroup
from src.presentation.resources import strings


def get_state_str(order: OrderEntity) -> str:
    if order.state == OrderState.PENDING:
        return strings.EMPLOYEE.ORDER.STATES.PENDING
    elif order.state == OrderState.COOKING:
        return strings.EMPLOYEE.ORDER.STATES.COOKING
    elif order.state == OrderState.READY and order.pickup_code:
        return strings.EMPLOYEE.ORDER.STATES.READY.format(code=order.pickup_code)
    elif order.state == OrderState.COMPLETED:
        return strings.EMPLOYEE.ORDER.STATES.COMPLETED
    elif order.state == OrderState.CANCELED and order.cancel_details:
        return strings.EMPLOYEE.ORDER.STATES.CANCELED.format(cancel_details=escape(order.cancel_details))
    else:
        raise ValueError('Unexpected order state.')


async def show_order_view(bot: Bot, chat_id: int, order: OrderEntity) -> Message:
    if order.state_group == OrderStateGroup.IN_PROGRESS:
        text = strings.EMPLOYEE.ORDER.IN_PROGRESS_VIEW
    elif order.state_group == OrderStateGroup.CLOSED:
        text = strings.EMPLOYEE.ORDER.CLOSED_VIEW
    else:
        raise ValueError('Unexpected order state group.')

    text = text.format(
        id=order.id,
        state=get_state_str(order),
        nickname=escape(order.client.client_name) if order.client.client_name else strings.EMPLOYEE.ORDER.NO_NICKNAME,
        client_id=order.client_id,
        date=order.date_create.strftime('%d.%m.%Y %H:%M:%S'),
        details=escape(order.details),
    )
    return await bot.send_message(chat_id, text)

