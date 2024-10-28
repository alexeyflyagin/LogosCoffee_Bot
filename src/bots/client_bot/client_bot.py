from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from src import config
from src.bots.user_state_storage import storage
from src.bots.client_bot.handlers import handler

async def start_bot():
    try:
        bot = Bot(config.CLIENT_BOT_TOKEN)
        dp = Dispatcher(storage=storage)
        dp.include_routers(handler.router)
        print(f"{__name__} is started.")
        await dp.start_polling(bot)
    except CancelledError:
        print(f"{__name__} is finished.")
