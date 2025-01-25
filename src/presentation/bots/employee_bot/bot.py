from asyncio import CancelledError
from datetime import datetime

from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramBadRequest

from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.events.channels import NEW_ORDER
from src.data.logoscoffee.events.notifier import EventNotifier
from src.data.logoscoffee.exceptions import DatabaseError, UnknownError
from src.presentation.bots.bot import BaseBot
from src.presentation.bots.employee_bot import constants
from src.presentation.bots.employee_bot.handlers import handler, end_handler

from src.presentation.bots.employee_bot.views.models.order import OrderViewData
from src.presentation.bots.employee_bot.views.order import view__order
from src.presentation.bots.view_system.utils import show_view


class EmployeeBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher, event_notifier: EventNotifier):
        super().__init__(bot, dp, "Employee")
        self._event_notifier: EventNotifier = event_notifier
        self._event_notifier.add_listener(NEW_ORDER, self.__new_order_listener)

    async def run(self):
        try:
            self.dp.include_routers(handler.router, end_handler.router)
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except CancelledError:
            self.shutdown()

    async def __new_order_listener(self, order: OrderEntity):
        try:
            subscribers = await handler.event_service.get_subscribers(constants.EVENT__NEW_ORDER)
            for subscriber in subscribers:
                try:
                    await show_view(self.bot, subscriber.chat_id, view__order(OrderViewData.from_order_entity(order)))
                except TelegramBadRequest:
                    pass
        except (DatabaseError, UnknownError):
            pass
