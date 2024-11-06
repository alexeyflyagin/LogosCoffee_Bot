from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from loguru import logger

import config
from presentation.user_state_storage import storage
from presentation.client_bot.handlers import handler, review_handler, authorization_handler, end_handler


async def start_bot():
    try:
        bot = Bot(config.CLIENT_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
        dp = Dispatcher(storage=storage)
        dp.include_routers(handler.router, authorization_handler.router, review_handler.router,
                           end_handler.router)
        logger.info(f"Client bot is started.")
        await dp.start_polling(bot)
    except CancelledError:
        logger.info(f"Client bot is finished.")
