from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from loguru import logger

import config
from bots.user_state_storage import storage
from bots.client_bot.handlers import handler


async def start_bot():
    try:
        bot = Bot(config.CLIENT_BOT_TOKEN)
        dp = Dispatcher(storage=storage)
        dp.include_routers(handler.router)
        logger.info(f"{__name__} is started.")
        await dp.start_polling(bot)
    except CancelledError:
        logger.info(f"{__name__} is finished.")
