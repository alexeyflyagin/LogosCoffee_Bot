import asyncio
from asyncio import CancelledError
from datetime import datetime
from html import escape

from aiogram import Bot, Dispatcher
from loguru import logger

from src.data.logoscoffee.exceptions import UnknownError, DatabaseError
from src.presentation.bots.admin_bot import constants
from src.presentation.bots.admin_bot.handlers import handler, announcement_handler, end_handler
from src.presentation.bots.bot import BaseBot
from src.presentation.resources import strings


class AdminBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher):
        super().__init__(bot, dp)


    async def run(self):
        try:
            self.dp.include_routers(handler.router, announcement_handler.router, end_handler.router)
            await self.bot.delete_webhook(drop_pending_updates=True)
            logger.info(f"Admin bot is started.")
            await asyncio.gather(
                self.__new_review_polling(),
                self.dp.start_polling(self.bot),
            )
        except CancelledError:
            logger.info(f"Admin bot is finished.")

    async def __new_review_polling(self):
        last_update_time = datetime.now()
        while True:
            try:
                reviews = await handler.admin_service.get_new_reviews(last_update_time)
                last_update_time = datetime.now()
                if reviews:
                    subscribers = await handler.event_service.get_subscribers(constants.EVENT__NEW_REVIEW)
                    for review in reviews:
                        for subscriber in subscribers:
                            text = strings.ADMIN.NEW_REVIEW_NOTIFICATION.format(review_content=escape(review.text_content))
                            await self.bot.send_message(chat_id=subscriber.chat_id, text=text)
            except (DatabaseError, UnknownError, Exception):
                pass
            await asyncio.sleep(1)

