from datetime import datetime
from html import escape

from pydantic import BaseModel

from src.data.logoscoffee.entities.orm_entities import MenuEntity
from src.presentation.bots.views.admin.keyboards.menu import EMPTY_MENU_IKM
from src.presentation.bots.views.models import View, ViewType
from src.presentation.resources import strings


class MenuViewData(BaseModel):
    id: int
    last_date_update: datetime
    text_content: str | None

    @staticmethod
    def from_entity(entity: MenuEntity) -> "MenuViewData":
        if not isinstance(entity, MenuEntity):
            raise ValueError("Incorrect type of the args.")

        return MenuViewData(
            id=entity.id,
            last_date_update=entity.last_date_update,
            text_content=entity.text_content,
        )

    def view(self):
        text = escape(self.text_content) if self.text_content else strings.ADMIN.EMPTY_MENU_CONTENT
        markup = None if self.text_content else EMPTY_MENU_IKM
        return View(view_type=ViewType.TEXT, text=text, reply_markup=markup)
