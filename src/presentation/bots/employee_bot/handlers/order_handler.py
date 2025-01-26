from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, InvalidTokenError
from src.data.logoscoffee.interfaces.employee_order_service import EmployeeOrderService
from src.loggers import bot_logger as logger
from src.presentation.bots.employee_bot.constants import Tag
from src.presentation.bots.employee_bot.handlers.utils import get_token, unknown_error_for_callback, invalid_token_error
from src.presentation.bots.views.employee.callbacks.order import OrderCD

router = Router(name=__name__)
order_service: EmployeeOrderService


@router.callback_query(OrderCD.filter())
async def next_state__handler(callback: CallbackQuery, state: FSMContext):
    try:
        data = OrderCD.unpack(callback.data)
        token = await get_token(state)
        # confirmation_markup(Tag.NEXT_ORDER_CONFIRMATION)
    except InvalidTokenError as e:
        logger.debug(e)
        await invalid_token_error(callback.message, state)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.error(e)
        await unknown_error_for_callback(callback, state)
