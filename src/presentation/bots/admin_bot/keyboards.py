from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.bots.admin_bot import constants
from src.presentation.resources import strings

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=strings.BTN.WRITE_ANNOUNCEMENT), KeyboardButton(text=strings.BTN.MY_ANNOUNCEMENTS)],
        [KeyboardButton(text=strings.BTN.REVIEWS)],
    ], resize_keyboard=True, input_field_placeholder=strings.GENERAL.SELECT_ACTION,
)


class AnnouncementCD(CallbackData, prefix=constants.CD_PREFIX__Announcement):
    announcement_id: int
    action: int

    class Action:
        PUBLISH = 0
        DELETE = 1
        SHOW = 2


def announcement_markup(announcement_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    publish_data = AnnouncementCD(announcement_id=announcement_id, action=AnnouncementCD.Action.PUBLISH).pack()
    delete_data = AnnouncementCD(announcement_id=announcement_id, action=AnnouncementCD.Action.DELETE).pack()
    show_data = AnnouncementCD(announcement_id=announcement_id, action=AnnouncementCD.Action.SHOW).pack()
    ikb.add(InlineKeyboardButton(text=strings.BTN.DISTRIBUTE, callback_data=publish_data))
    ikb.add(InlineKeyboardButton(text=strings.BTN.SHOW, callback_data=show_data))
    ikb.add(InlineKeyboardButton(text=strings.BTN.DELETE, callback_data=delete_data))
    ikb.adjust(1, 2)
    return ikb.as_markup()
