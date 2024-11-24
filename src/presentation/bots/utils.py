from datetime import datetime
from decimal import Decimal
from html import escape

from aiogram import Bot
from loguru import logger

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, URLInputFile

from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity
from src.presentation.bots.types import FileAddress
from src.presentation.resources import strings
from src.presentation.resources.strings_builder import strings_builder


def get_datetime_str(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")


def get_date_last_announcement_distributing_str(announcement: AnnouncementEntity):
    if announcement.date_last_distribute:
        return strings_builder.b(get_datetime_str(announcement.date_last_distribute))
    return strings_builder.i(strings.GENERAL.NO_DATA)

async def send_or_update_msg(msg: Message, text: str, is_update: bool = False, replay_markup = None) -> Message:
    try:
        if is_update:
            send_msg = await msg.edit_text(text=text, reply_markup=replay_markup)
        else:
            send_msg = await msg.answer(text=text, reply_markup=replay_markup)
        return send_msg
    except TelegramBadRequest as e:
        logger.warning(e)


def get_link_to_file_by_path(bot_token: str, file_path: str) -> str:
    return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

def to_rubles(money: Decimal) -> str:
    return f"{money:.2f} ₽"

async def send_announcement(bot: Bot, chat_id: int, announcement: AnnouncementEntity):
    text = announcement.text_content
    if announcement.preview_photo:
        address = FileAddress.from_address(announcement.preview_photo)
        file = await Bot(address.bot_type.value, session=bot.session).get_file(address.file_id)
        photo = URLInputFile(get_link_to_file_by_path(bot_token=address.bot_type.value, file_path=file.file_path))
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=text, parse_mode=None)
    else:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=None)
