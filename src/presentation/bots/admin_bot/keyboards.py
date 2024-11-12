from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.bots.admin_bot import constants
from src.presentation.resources import strings

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=strings.BTN.WRITE_PROMOTIONAL_OFFER)],
        [KeyboardButton(text=strings.BTN.REVIEWS)]
    ], resize_keyboard=True, input_field_placeholder=strings.GENERAL.SELECT_ACTION,
)


class OfferCD(CallbackData, prefix=constants.CD_PREFIX__PROMOTIONAL_OFFER):
    offer_id: int
    action: int

    class Action:
        PUBLISH = 0
        DELETE = 1
        SHOW = 2


def offer_markup(offer_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    publish_data = OfferCD(offer_id=offer_id, action=OfferCD.Action.PUBLISH).pack()
    delete_data = OfferCD(offer_id=offer_id, action=OfferCD.Action.DELETE).pack()
    show_data = OfferCD(offer_id=offer_id, action=OfferCD.Action.SHOW).pack()
    ikb.add(InlineKeyboardButton(text=strings.BTN.DISTRIBUTE, callback_data=publish_data))
    ikb.add(InlineKeyboardButton(text=strings.BTN.SHOW, callback_data=show_data))
    ikb.add(InlineKeyboardButton(text=strings.BTN.DELETE, callback_data=delete_data))
    ikb.adjust(1, 2)
    return ikb.as_markup()
