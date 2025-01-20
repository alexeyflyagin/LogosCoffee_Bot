from asyncio import CancelledError
from loguru import logger

from aiogram import Dispatcher, Bot

from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.events.channels import NEW_ORDER
from src.data.logoscoffee.events.notifier import EventNotifier
from src.presentation.bots.bot import BaseBot


class EmployeeBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher, event_notifier: EventNotifier):
        super().__init__(bot, dp, "Employee")
        self._event_notifier: EventNotifier = event_notifier
        self._event_notifier.add_listener(NEW_ORDER, self.__new_order_listener)


    async def run(self):
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except CancelledError:
            self.shutdown()

    async def __new_order_listener(self, order: OrderEntity):
        logger.debug(order.__repr__())
        # TODO listener handling
