from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.data.logoscoffee.interfaces.employee_order_service import EmployeeOrderService
from src.presentation.bots.employee_bot.handlers.utils import get_token
from src.presentation.bots.views.employee.callbacks.order import OrderCD

router = Router(name=__name__)
order_service: EmployeeOrderService


@router.callback_query(OrderCD.filter())
async def next_state__handler(callback: CallbackQuery, state: FSMContext):
    data = OrderCD.unpack(callback.data)
    token = await get_token(state)
    # confirmation_markup(Tag.NEXT_ORDER_CONFIRMATION)
