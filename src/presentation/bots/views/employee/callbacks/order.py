from enum import IntEnum

from aiogram.filters.callback_data import CallbackData

from src.presentation.bots.views.employee.constants import Prefix


class OrderCD(CallbackData, prefix=Prefix.ORDER):
    order_id: int
    action: "Action"

    class Action(IntEnum):
        NEXT_STATE = 0
        REJECT = 1
