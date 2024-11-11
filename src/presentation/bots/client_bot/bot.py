import asyncio
from asyncio import CancelledError
from datetime import datetime
from time import sleep

from aiogram import Bot, Dispatcher
from aiogram.types import URLInputFile
from loguru import logger

from src.presentation.bots.bot import BaseBot
from src.presentation.bots.client_bot import constants
from src.presentation.bots.client_bot.handlers import handler, review_handler, authorization_handler, end_handler


class ClientBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher):
        super().__init__(bot, dp)

    async def run(self):
        try:
            self.dp.include_routers(
                handler.router,
                authorization_handler.router,
                review_handler.router,
                end_handler.router
            )
            await self.bot.delete_webhook(drop_pending_updates=True)
            logger.info(f"Client bot is started.")
            await asyncio.gather(
                self.dp.start_polling(self.bot),
                self.__offer_pooling(),
            )
        except CancelledError:
            logger.info(f"Client bot is finished.")

    async def __offer_pooling(self):
        last_update_time = datetime.now()
        while True:
            try:
                offers = await authorization_handler.client_service.get_new_offers(last_update_time)
                last_update_time = datetime.now()
                logger.debug(offers)
                if offers:
                    subscribers = await authorization_handler.event_service.get_subscribers(constants.EVENT__NEW_OFFER)
                    for offer in offers:
                        for subscriber in subscribers:
                            if offer.preview_photo_url:
                                photo = URLInputFile(offer.preview_photo_url)
                                await self.bot.send_photo(subscriber.user_state.chat_id, photo, caption=offer.text_content)
                            else:
                                await self.bot.send_message(subscriber.user_state.chat_id, offer.text_content)
            except Exception as e:
                logger.error(e)
            await asyncio.sleep(1)

