from aiogram.filters.callback_data import CallbackData

from src.presentation.bots.views.admin.constants import Prefix


class AnnouncementCD(CallbackData, prefix=Prefix.ANNOUNCEMENT):
    announcement_id: int
    action: int

    class Action:
        PUBLISH = 0
        SHOW = 1
