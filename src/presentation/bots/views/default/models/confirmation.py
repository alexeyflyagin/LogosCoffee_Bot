from aiogram.enums import ParseMode
from pydantic import BaseModel

from src.presentation.bots.views.default.keyboards.confirmation import confirmation_ikm
from src.presentation.bots.views.models import View, ViewType


class ConfirmationViewData(BaseModel):
    text: str
    tag: int
    parse_mode: ParseMode | None = None
    p_arg: int | str | bool | None = None
    s_arg: int | str | bool | None = None

    def view(self) -> View:
        markup = confirmation_ikm(self.tag, self.p_arg, self.s_arg)
        return View(view_type=ViewType.TEXT, text=self.text, parse_mode=self.parse_mode, reply_markup=markup)
