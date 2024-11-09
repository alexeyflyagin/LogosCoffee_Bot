from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from loguru import logger

from src.presentation.bots.bot import BaseBot
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
            await self.dp.start_polling(self.bot)
        except CancelledError:
            logger.info(f"Client bot is finished.")
