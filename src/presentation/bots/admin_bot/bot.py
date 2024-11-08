from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
from src.presentation.bots.admin_bot.handlers import handler

async def run(token: str, dp: Dispatcher):
    try:
        default = DefaultBotProperties(parse_mode=ParseMode.HTML)
        bot = Bot(token, default=default)
        dp.include_routers(handler.router)
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info(f"Admin bot is started.")
        await dp.start_polling(bot)
    except CancelledError:
        logger.info(f"Admin bot is finished.")
