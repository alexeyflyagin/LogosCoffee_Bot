from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.presentation.resources import strings


MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=strings.BTN.READ_REVIEWS), KeyboardButton(text=strings.BTN.WRITE_PROMOTIONAL_OFFER)]], resize_keyboard=True
)
