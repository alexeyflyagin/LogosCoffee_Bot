from datetime import datetime
from html import escape

from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger
from bs4 import BeautifulSoup

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, URLInputFile, InlineKeyboardMarkup, InlineKeyboardButton

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
        logger.error(e)


def get_link_to_file_by_path(bot_token: str, file_path: str) -> str:
    return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

def get_announcement_markup(announcement: AnnouncementEntity) -> InlineKeyboardMarkup | None:
    if not announcement.text_content:
        return None
    soup = BeautifulSoup(announcement.text_content, 'html.parser')
    url_arg = 'url'
    url_button_tags = soup.find_all('button', {url_arg: True})
    if not url_button_tags:
        return None
    ikb = InlineKeyboardBuilder()
    adjust = []
    for tag in url_button_tags:
        button_url = tag.get(url_arg)
        button_text = tag.text or "Link"
        ikb.add(InlineKeyboardButton(text=button_text, url=button_url))
        adjust.append(1)
    ikb.adjust(*adjust)
    return ikb.as_markup()

def decompose_custom_tags(text: str | None) -> str | None:
    if not text:
        return text
    soup = BeautifulSoup(text, 'html.parser')
    url_arg = 'url'
    url_button_tags = soup.find_all('button', {url_arg: True})
    if not url_button_tags:
        return text
    for tag in url_button_tags:
        tag.decompose()
    return soup.text


async def send_announcement(bot: Bot, chat_id: int, announcement: AnnouncementEntity):
    markup = get_announcement_markup(announcement)
    text = decompose_custom_tags(announcement.text_content)
    if announcement.preview_photo:
        address = FileAddress.from_address(announcement.preview_photo)
        file = await Bot(address.bot_type.value, session=bot.session).get_file(address.file_id)
        photo = URLInputFile(get_link_to_file_by_path(bot_token=address.bot_type.value, file_path=file.file_path))
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=escape(text), reply_markup=markup)
    else:
        if text.strip() == "":
            text = "ㅤ"
        await bot.send_message(chat_id=chat_id, text=escape(text), reply_markup=markup)
