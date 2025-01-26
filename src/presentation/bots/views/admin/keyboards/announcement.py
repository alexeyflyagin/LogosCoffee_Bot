from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.bots.views.admin.callbacks.announcement import AnnouncementCD
from src.presentation.resources import strings


def announcement_ikm(announcement_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    publish_data = AnnouncementCD(announcement_id=announcement_id, action=AnnouncementCD.Action.PUBLISH).pack()
    show_data = AnnouncementCD(announcement_id=announcement_id, action=AnnouncementCD.Action.SHOW).pack()
    ikb.add(InlineKeyboardButton(text=strings.BTN.DISTRIBUTE, callback_data=publish_data))
    ikb.add(InlineKeyboardButton(text=strings.BTN.SHOW, callback_data=show_data))
    ikb.adjust(1, 1)
    return ikb.as_markup()
