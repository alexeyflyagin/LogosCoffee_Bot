import random
from typing import Any

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.resources import strings

PREFIX__CONFIRMATION = "cnfrm"

class ConfirmationCD(CallbackData, prefix=PREFIX__CONFIRMATION):
    tag: str
    p_arg: Any
    s_arg: Any
    action: int

    class Action:
        CANCEL = 0
        CONFIRM = 1


def confirmation_markup(tag: str, p_arg: Any = None, s_arg: Any = None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    confirm_data = ConfirmationCD(tag=tag, p_arg=p_arg, s_arg=s_arg, action=ConfirmationCD.Action.CONFIRM).pack()
    cancel_data = ConfirmationCD(tag=tag, p_arg=p_arg, s_arg=s_arg, action=ConfirmationCD.Action.CANCEL).pack()
    buttons = [
        InlineKeyboardButton(text=strings.BTN.CONFIRM, callback_data=confirm_data),
        InlineKeyboardButton(text=strings.BTN.CANCEL, callback_data=cancel_data),
    ]
    random.shuffle(buttons)
    ikb.add(*buttons)
    ikb.adjust(2)
    return ikb.as_markup()

