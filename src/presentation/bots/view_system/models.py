from enum import Enum

from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from pydantic import BaseModel, Field


class ViewType(str, Enum):
    TEXT = "text"


class View(BaseModel):
    view_type: ViewType = Field(default=ViewType.TEXT)
    text: str | None = Field(default=None)
    parse_mode: ParseMode | None = Field(default=None)
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = Field(
        default=None)
