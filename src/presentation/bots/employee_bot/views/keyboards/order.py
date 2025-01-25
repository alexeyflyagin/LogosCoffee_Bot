from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.data.logoscoffee.enums import OrderState, OrderStateGroup
from src.presentation.bots.employee_bot.views.callbacks.order import OrderCD
from src.presentation.bots.employee_bot.views.models.order import OrderViewData
from src.presentation.resources import strings


def get_next_state_btn_str(state: OrderState):
    if state == OrderState.PENDING:
        return strings.EMPLOYEE.ORDER.BTN.ORDER_CONFIRM
    elif state == OrderState.COOKING:
        return strings.EMPLOYEE.ORDER.BTN.ORDER_READY
    elif state == OrderState.READY:
        return strings.EMPLOYEE.ORDER.BTN.ORDER_COMPLETE
    else:
        raise ValueError('Unexpected order state.')


def order_ikm(data: OrderViewData) -> InlineKeyboardMarkup | None:
    ikb = InlineKeyboardBuilder()
    if data.state_group == OrderStateGroup.CLOSED:
        return None
    next_state_data = OrderCD(order_id=data.id, action=OrderCD.Action.NEXT_STATE).pack()
    reject_data = OrderCD(order_id=data.id, action=OrderCD.Action.REJECT).pack()
    ikb.add(InlineKeyboardButton(text=strings.EMPLOYEE.ORDER.BTN.ORDER_REJECT, callback_data=reject_data))
    ikb.add(InlineKeyboardButton(text=get_next_state_btn_str(data.state), callback_data=next_state_data))
    ikb.adjust(2)
    return ikb.as_markup()

