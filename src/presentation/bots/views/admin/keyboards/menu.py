from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.presentation.bots.admin_bot.constants import CHANGE_MENU_CD
from src.presentation.resources import strings

EMPTY_MENU_IKM = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=strings.BTN.CHANGE_MENU, callback_data=CHANGE_MENU_CD)]
    ],
)
