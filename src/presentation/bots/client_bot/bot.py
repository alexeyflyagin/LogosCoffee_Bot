from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from src.presentation.bots.client_bot.handlers import handler, review_handler, authorization_handler, end_handler


async def run(token: str, dp: Dispatcher):
    try:
        default = DefaultBotProperties(parse_mode=ParseMode.HTML)
        bot = Bot(token, default=default)
        dp.include_routers(
            handler.router,
            authorization_handler.router,
            review_handler.router,
            end_handler.router
        )
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info(f"Client bot is started.")
        await dp.start_polling(bot)
    except CancelledError:
        logger.info(f"Client bot is finished.")
