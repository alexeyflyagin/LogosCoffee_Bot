from aiogram.filters.callback_data import CallbackData

from src.presentation.bots.employee_bot.views import prefixes


class OrderCD(CallbackData, prefix=prefixes.ORDER):
    order_id: int
    action: int

    class Action:
        NEXT_STATE = 0
        REJECT = 1
