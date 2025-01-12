from asyncio import CancelledError

from aiogram import Dispatcher, Bot
from src.presentation.bots.bot import BaseBot


class EmployeeBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher):
        super().__init__(bot, dp, "Employee")

    async def run(self):
        try:
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except CancelledError:
            self.shutdown()
