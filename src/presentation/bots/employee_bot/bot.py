from asyncio import CancelledError

from aiogram import Dispatcher, Bot
from loguru import logger

from src.presentation.bots.bot import BaseBot
from src.presentation.bots.employee_bot.handlers import handler


class EmployeeBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher):
        super().__init__(bot, dp)

    async def run(self):
        try:
            self.dp.include_routers(handler.router)
            await self.bot.delete_webhook(drop_pending_updates=True)
            logger.info(f"Employee bot is started.")
            await self.dp.start_polling(self.bot)
        except CancelledError:
            logger.info(f"Employee bot is finished.")
