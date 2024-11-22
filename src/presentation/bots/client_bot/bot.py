import asyncio
from asyncio import CancelledError
from datetime import datetime
from html import escape

from aiogram import Bot, Dispatcher
from aiogram.types import URLInputFile
from loguru import logger

from src.presentation.bots.bot import BaseBot
from src.presentation.bots.client_bot import constants
from src.presentation.bots.client_bot.handlers import handler, review_handler, authorization_handler, end_handler, \
    menu_handler
from src.presentation.bots.client_bot.handlers import draft_order_handler
from src.presentation.bots.utils import send_announcement


class ClientBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher):
        super().__init__(bot, dp)

    async def run(self):
        try:
            self.dp.include_routers(
                handler.router,
                authorization_handler.router,
                review_handler.router,
                menu_handler.router,
                draft_order_handler.router,
                end_handler.router
            )
            await self.bot.delete_webhook(drop_pending_updates=True)
            logger.info(f"Client bot is started.")
            await asyncio.gather(
                self.__announcement_pooling(),
                self.dp.start_polling(self.bot),
            )
        except CancelledError:
            logger.info(f"Client bot is finished.")

    async def __announcement_pooling(self):
        last_update_time = datetime.now()
        while True:
            try:
                announcements = await authorization_handler.client_service.get_new_announcements(last_update_time)
                last_update_time = datetime.now()
                if announcements:
                    subscribers = await handler.event_service.get_subscribers(constants.EVENT__NEW_ANNOUNCEMENT)
                    for announcement in announcements:
                        for subscriber in subscribers:
                            await send_announcement(self.bot, chat_id=subscriber.chat_id, announcement=announcement)
            except Exception as e:
                logger.error(e)
            await asyncio.sleep(1)
