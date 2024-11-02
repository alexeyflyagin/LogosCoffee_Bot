from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from loguru import logger

import config
from presentation.user_state_storage import storage
from presentation.client_bot.handlers import handler


async def start_bot():
    try:
        bot = Bot(config.CLIENT_BOT_TOKEN)
        dp = Dispatcher(storage=storage)
        dp.include_routers(handler.router)
        logger.info(f"Client bot is started.")
        await dp.start_polling(bot)
    except CancelledError:
        logger.info(f"Client bot is finished.")
