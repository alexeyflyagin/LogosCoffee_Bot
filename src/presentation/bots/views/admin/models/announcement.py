from datetime import datetime

from aiogram.enums import ParseMode
from pydantic import BaseModel

from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity
from src.presentation.bots.utils import get_datetime_str
from src.presentation.bots.views.admin.keyboards.announcement import announcement_ikm
from src.presentation.bots.views.models import View, ViewType
from src.presentation.resources import strings
from src.presentation.resources.strings_builder.strings_builder import b, i


class AnnouncementViewData(BaseModel):
    id: int
    date_create: datetime
    date_last_distribute: datetime | None
    text_content: str | None
    preview_photo_data: str | None

    @staticmethod
    def from_entity(entity: AnnouncementEntity) -> "AnnouncementViewData":
        if not isinstance(entity, AnnouncementEntity):
            raise ValueError("Incorrect type of the args.")

        return AnnouncementViewData(
            id=entity.id,
            date_create=entity.date_create,
            date_last_distribute=entity.date_last_distribute,
            text_content=entity.text_content,
            preview_photo_data=entity.preview_photo_data,
        )

    def view(self) -> View:
        markup = announcement_ikm(self.id)
        _date_last_distribute = i(strings.GENERAL.NO_DATA)
        if self.date_last_distribute:
            _date_last_distribute = b(get_datetime_str(self.date_last_distribute))
        text = strings.ADMIN.ANNOUNCEMENT.MAIN.format(
            announcement_id=self.id,
            date_last_distribute=_date_last_distribute,
            date_create=get_datetime_str(self.date_create)
        )
        return View(view_type=ViewType.TEXT, text=text, parse_mode=ParseMode.HTML, reply_markup=markup)
