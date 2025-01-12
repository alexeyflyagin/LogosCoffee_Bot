from asyncio import CancelledError

from aiogram import Dispatcher, Bot
from src.presentation.bots.bot import BaseBot
from src.presentation.bots.employee_bot.handlers import handler


class EmployeeBot(BaseBot):

    def __init__(self, bot: Bot, dp: Dispatcher):
        super().__init__(bot, dp, "Employee")

    async def run(self):
        try:
            self.dp.include_routers(handler.router)
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except CancelledError:
            self.shutdown()
