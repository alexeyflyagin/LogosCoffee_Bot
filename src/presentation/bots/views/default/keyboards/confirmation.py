import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.bots.views.default.callbacks.confirmation import ConfirmationCD
from src.presentation.resources import strings


def confirmation_ikm(
        tag: int,
        p_arg: int | str | bool | None = None,
        s_arg: int | str | bool | None = None,
) -> InlineKeyboardMarkup:
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
