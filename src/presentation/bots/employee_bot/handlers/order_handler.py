from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.data.logoscoffee.enums import OrderStateGroup
from src.data.logoscoffee.exceptions import OrderNotFoundError, OrderStateError
from src.data.logoscoffee.interfaces.employee_order_service import EmployeeOrderService
from src.loggers import bot_logger
from src.presentation.bots.employee_bot import constants
from src.presentation.bots.employee_bot.handlers.utils import get_token
from src.presentation.bots.views.default.callbacks.confirmation import ConfirmationCD
from src.presentation.bots.views.default.keyboards.confirmation import confirmation_ikm
from src.presentation.bots.views.default.models.confirmation import ConfirmationViewData
from src.presentation.bots.views.employee.callbacks.order import OrderCD
from src.presentation.bots.views.employee.models.order import OrderViewData
from src.presentation.resources import strings

router = Router(name=__name__)
order_service: EmployeeOrderService


@router.callback_query(OrderCD.filter())
async def next_state__handler(callback: CallbackQuery, state: FSMContext):
    try:
        data = OrderCD.unpack(callback.data)
        token = await get_token(state)
        await order_service.get_order_by_id(token, data.order_id)
        if data.action == OrderCD.Action.NEXT_STATE:
            await ConfirmationViewData(
                text=strings.EMPLOYEE.ORDER.NEXT_STATE_CONFIRMATION_VIEW.format(order_id=data.order_id),
                tag=constants.Tag.NEXT_ORDER_CONFIRMATION,
                parse_mode=ParseMode.HTML,
                p_arg=data.order_id,
            ).view().edit_view(callback.message)
        else:
            raise TypeError("Unexpected action")
    except OrderNotFoundError as e:
        bot_logger.debug(e)
        await callback.message.edit_text(strings.EMPLOYEE.ORDER.NOT_FOUND_ERROR)




@router.callback_query(ConfirmationCD.filter(F.tag == constants.Tag.NEXT_ORDER_CONFIRMATION))
async def next_state__confirmation__handler(callback: CallbackQuery, state: FSMContext):
    try:
        data = ConfirmationCD.unpack(callback.data)
        order_id = int(data.p_arg)
        token = await get_token(state)
        if data.action == ConfirmationCD.Action.CONFIRM:
            try:
                order = await order_service.next_order_state(token, order_id)
            except OrderStateError:
                order = await order_service.get_order_by_id(token, order_id)
                await callback.answer(text=strings.EMPLOYEE.ORDER.INCORRECT_STATE, show_alert=True)
            await OrderViewData.from_order_entity(order).view().edit_view(callback.message)
        elif data.action == ConfirmationCD.Action.CANCEL:
            order = await order_service.get_order_by_id(token, order_id)
            await OrderViewData.from_order_entity(order).view().edit_view(callback.message)
        else:
            raise TypeError("Unexpected action")
    except OrderNotFoundError as e:
        bot_logger.debug(e)
        await callback.message.edit_text(strings.EMPLOYEE.ORDER.NOT_FOUND_ERROR)
