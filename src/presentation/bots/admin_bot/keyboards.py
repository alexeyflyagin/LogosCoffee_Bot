from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.presentation.resources import strings

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=strings.BTN.MENU), KeyboardButton(text=strings.BTN.CHANGE_MENU)],
        [KeyboardButton(text=strings.BTN.WRITE_ANNOUNCEMENT)],
    ], resize_keyboard=True, input_field_placeholder=strings.GENERAL.SELECT_ACTION,
)
