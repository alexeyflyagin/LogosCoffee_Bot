from datetime import datetime
from decimal import Decimal
from html import escape

from aiogram import Bot
from loguru import logger

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, URLInputFile

from src.data.logoscoffee.entities.orm_entities import OrderEntity

async def send_order_info(bot: Bot, chat_id: int, order: OrderEntity):
    pass #TODO