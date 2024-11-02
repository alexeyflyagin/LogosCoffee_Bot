from asyncio import CancelledError

from aiogram import Dispatcher, Bot
from loguru import logger

import config
from presentation.employee_bot.handlers import handler
from presentation.user_state_storage import storage


async def start_bot():
    try:
        bot = Bot(config.EMPLOYEE_BOT_TOKEN)
        dp = Dispatcher(storage=storage)
        dp.include_routers(handler.router)
        logger.info(f"Employee bot is started.")
        await dp.start_polling(bot)
    except CancelledError:
        logger.info(f"Employee bot is finished.")
