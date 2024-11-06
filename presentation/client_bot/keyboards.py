from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from presentation import strings

AUTHORIZATION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN_AUTHORIZE, request_contact=True)]], resize_keyboard=True
)
