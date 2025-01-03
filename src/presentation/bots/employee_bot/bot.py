import asyncio
from asyncio import CancelledError
from datetime import datetime

from aiogram import Dispatcher, Bot
from loguru import logger

from src.presentation.bots.bot import BaseBot
from src.presentation.bots.employee_bot import constants
from src.presentation.bots.employee_bot.handlers import handler
from src.presentation.bots.employee_bot.handlers.utils import send_order_info


class EmployeeBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher):
        super().__init__(bot, dp, "Employee")

    async def run(self):
        try:
            self.dp.include_routers(handler.router)
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except CancelledError:
            self.shutdown()

    async def __new_orders_pooling(self):
        last_update_time = datetime.now()
        while True:
            try:
                orders = await handler.employee_service.get_new_orders(last_update_time)
                last_update_time = datetime.now()
                if orders:
                    subscribers = await handler.event_service.get_subscribers(constants.EVENT__NEW_ORDER)
                    for order in orders:
                        for subscriber in subscribers:
                            await send_order_info(self.bot, chat_id=subscriber.chat_id, order=order)
            except Exception as e:
                logger.error(e)
            await asyncio.sleep(1)
