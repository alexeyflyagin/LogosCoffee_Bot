from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.presentation.resources import strings

AUTHORIZATION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN.AUTHORIZE, request_contact=True)]], resize_keyboard=True,
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=strings.BTN.MENU)],
        [KeyboardButton(text=strings.BTN.WRITE_REVIEW)],
    ], resize_keyboard=True,
    input_field_placeholder=strings.GENERAL.SELECT_ACTION,
)
