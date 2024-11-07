from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from loguru import logger

import config
from presentation.admin_bot.handlers import handler
from presentation.user_state_storage import storage


async def start_bot():
    try:
        bot = Bot(config.ADMIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
        dp = Dispatcher(storage=storage)
        dp.include_routers(handler.router)
        logger.info(f"Admin bot is started.")
        await dp.start_polling(bot)
    except CancelledError:
        logger.info(f"Admin bot is finished.")
