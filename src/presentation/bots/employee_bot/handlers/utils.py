from aiogram import Bot

from src.data.logoscoffee.entities.orm_entities import OrderEntity

async def send_order_info(bot: Bot, chat_id: int, order: OrderEntity):
    pass #TODO