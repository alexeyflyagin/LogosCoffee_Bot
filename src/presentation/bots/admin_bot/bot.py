from asyncio import CancelledError
from html import escape

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest

from src.data.logoscoffee.entities.orm_entities import ReviewEntity
from src.data.logoscoffee.events.channels import NEW_REVIEW_CHANNEL
from src.data.logoscoffee.events.notifier import EventNotifier
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError
from src.presentation.bots.admin_bot import constants
from src.presentation.bots.admin_bot.handlers import handler, announcement_handler, end_handler
from src.presentation.bots.bot import BaseBot
from src.presentation.resources import strings


class AdminBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher, admin_token: str, event_notifier: EventNotifier):
        super().__init__(bot, dp, "Admin")
        self._admin_token: str = admin_token
        self._event_notifier: EventNotifier = event_notifier
        self._event_notifier.add_listener(NEW_REVIEW_CHANNEL, self.__new_review_listener)

    async def run(self):
        try:
            self.dp.include_routers(handler.router, announcement_handler.router, end_handler.router)
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except CancelledError:
            self.shutdown()

    async def __new_review_listener(self, review: ReviewEntity):
        try:
            subscribers = await handler.event_service.get_subscribers(constants.EVENT__NEW_REVIEW)
            for subscriber in subscribers:
                text = strings.ADMIN.NEW_REVIEW_NOTIFICATION.format(review_content=escape(review.text_content))
                try:
                    await self.bot.send_message(chat_id=subscriber.chat_id, text=text)
                except TelegramBadRequest:
                    pass
        except (DatabaseError, UnknownError):
            pass

