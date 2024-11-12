from datetime import datetime
from html import escape

from aiogram import Bot
from loguru import logger

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, URLInputFile

from src.data.logoscoffee.entities.orm_entities import PromotionalOfferEntity
from src.presentation.bots.types import FileAddress
from src.presentation.resources import strings
from src.presentation.resources.strings_builder import strings_builder


def get_datetime_str(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")


def get_date_last_offer_distributing_str(offer: PromotionalOfferEntity):
    if offer.date_last_distribute:
        return strings_builder.b(get_datetime_str(offer.date_last_distribute))
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



async def send_offer(bot: Bot, chat_id: int, offer: PromotionalOfferEntity):
    text = offer.text_content
    if offer.preview_photo:
        address = FileAddress.from_address(offer.preview_photo)
        file = await Bot(address.bot_token, session=bot.session).get_file(address.file_id)
        photo = URLInputFile(f"https://api.telegram.org/file/bot{address.bot_token}/{file.file_path}")
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=escape(text))
    else:
        await bot.send_message(chat_id=chat_id, text=escape(text))
