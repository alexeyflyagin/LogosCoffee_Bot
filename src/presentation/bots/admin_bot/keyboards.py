from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.bots.admin_bot import constants
from src.presentation.resources import strings


MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN.READ_REVIEWS), KeyboardButton(text=strings.BTN.WRITE_PROMOTIONAL_OFFER)]], resize_keyboard=True
)

class PromotionalOfferCD(CallbackData, prefix=constants.CD_PREFIX__PROMOTIONAL_OFFER):
    offer_id: int
    action: int

    class Action:
        PUBLISH = 0
        DELETE = 1


def promotional_offer_markup(offer_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    publish_data = PromotionalOfferCD(offer_id=offer_id, action=PromotionalOfferCD.Action.PUBLISH).pack()
    delete_data = PromotionalOfferCD(offer_id=offer_id, action=PromotionalOfferCD.Action.DELETE).pack()
    ikb.add(InlineKeyboardButton(text=strings.BTN.PUBLISH, callback_data=publish_data))
    ikb.add(InlineKeyboardButton(text=strings.BTN.DELETE, callback_data=delete_data))
    return ikb.as_markup()
