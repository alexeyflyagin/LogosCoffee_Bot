from aiogram.filters.callback_data import CallbackData

from src.presentation.bots.views.default.constants import Prefix


class ConfirmationCD(CallbackData, prefix=Prefix.CONFIRMATION):
    tag: int
    p_arg: int | str | bool | None
    s_arg: int | str | bool | None
    action: int

    class Action:
        CANCEL = 0
        CONFIRM = 1
