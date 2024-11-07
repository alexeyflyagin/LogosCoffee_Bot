from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from presentation import strings

AUTHORIZATION_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN.AUTHORIZE, request_contact=True)]], resize_keyboard=True
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN.WRITE_REVIEW)]], resize_keyboard=True
)
