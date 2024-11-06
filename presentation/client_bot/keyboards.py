from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from presentation import strings
from presentation.client_bot import command_strings

AUTHORIZATION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN_AUTHORIZE, request_contact=True)]], resize_keyboard=True
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=command_strings.MAKE_REVIEW)], [KeyboardButton(text="МЯУ")]], resize_keyboard=True
)
