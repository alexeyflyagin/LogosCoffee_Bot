from html import escape

from aiogram.enums import ParseMode

from src.data.logoscoffee.enums import OrderStateGroup, OrderState
from src.presentation.bots.employee_bot.views.keyboards.order import order_ikm
from src.presentation.bots.employee_bot.views.models.order import OrderViewData
from src.presentation.bots.view_system.models import View, ViewType
from src.presentation.resources import strings


def get_state_str(order_data: OrderViewData) -> str:
    if order_data.state == OrderState.PENDING:
        return strings.EMPLOYEE.ORDER.STATES.PENDING
    elif order_data.state == OrderState.COOKING:
        return strings.EMPLOYEE.ORDER.STATES.COOKING
    elif order_data.state == OrderState.READY and order_data.pickup_code:
        return strings.EMPLOYEE.ORDER.STATES.READY.format(code=order_data.pickup_code)
    elif order_data.state == OrderState.COMPLETED:
        return strings.EMPLOYEE.ORDER.STATES.COMPLETED
    elif order_data.state == OrderState.CANCELED and order_data.cancel_details:
        return strings.EMPLOYEE.ORDER.STATES.CANCELED.format(cancel_details=escape(order_data.cancel_details))
    else:
        raise ValueError('Unexpected order state.')


def view__order(data: OrderViewData) -> View:
    if data.state_group == OrderStateGroup.IN_PROGRESS:
        text = strings.EMPLOYEE.ORDER.IN_PROGRESS_VIEW
    elif data.state_group == OrderStateGroup.CLOSED:
        text = strings.EMPLOYEE.ORDER.CLOSED_VIEW
    else:
        raise ValueError('Unexpected order state group.')

    text = text.format(
        id=data.id,
        state=get_state_str(data),
        nickname=escape(data.client_nickname) if data.client_nickname else strings.EMPLOYEE.ORDER.NO_NICKNAME,
        client_id=data.client_id,
        date=data.date_create.strftime('%d.%m.%Y %H:%M:%S'),
        details=escape(data.details),
    )
    markup = order_ikm(data)

    return View(view_type=ViewType.TEXT, text=text, parse_mode=ParseMode.HTML, reply_markup=markup)
