import asyncio
from asyncio import CancelledError
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from loguru import logger

from src.data.logoscoffee.entities.orm_entities import AnnouncementEntity
from src.data.logoscoffee.events.channels import NEW_DISTRIBUTED_ANNOUNCEMENT
from src.data.logoscoffee.events.notifier import EventNotifier
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError
from src.presentation.bots.bot import BaseBot
from src.presentation.bots.client_bot import constants, commands
from src.presentation.bots.client_bot.handlers import handler, review_handler, authorization_handler, end_handler, \
    menu_handler, order_handler
from src.presentation.bots.utils import send_announcement


class ClientBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher, event_notifier: EventNotifier):
        super().__init__(bot, dp, "Client")
        self._event_notifier = event_notifier
        self._event_notifier.add_listener(NEW_DISTRIBUTED_ANNOUNCEMENT, self.__new_announcement_listener)

    async def run(self):
        try:
            self.dp.include_routers(
                handler.router,
                authorization_handler.router,
                review_handler.router,
                menu_handler.router,
                order_handler.router,
                end_handler.router
            )
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except CancelledError:
            self.shutdown()

    async def __new_announcement_listener(self, announcement: AnnouncementEntity):
        try:
            subscribers = await handler.event_service.get_subscribers(constants.EVENT__NEW_ANNOUNCEMENT)
            for subscriber in subscribers:
                try:
                    await send_announcement(self.bot, chat_id=subscriber.chat_id, announcement=announcement)
                except TelegramBadRequest:
                    pass
        except (UnknownError, DatabaseError):
            pass
