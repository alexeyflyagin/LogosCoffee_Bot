from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from src.presentation.bots import constants
from src.presentation.resources import strings

AUTHORIZATION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN.AUTHORIZE, request_contact=True)]], resize_keyboard=True,
)

EMPTY_DRAFT_ORDER_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=strings.BTN.MENU, callback_data=constants.CALLBACK_DATA__LIST_MENU)]],
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=strings.BTN.MENU)],
        [KeyboardButton(text=strings.BTN.DRAFT_ORDER)],
        [KeyboardButton(text=strings.BTN.WRITE_REVIEW)],
    ], resize_keyboard=True,
    input_field_placeholder=strings.GENERAL.SELECT_ACTION,
)
