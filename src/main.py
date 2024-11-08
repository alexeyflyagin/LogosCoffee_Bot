import asyncio
import sys
from asyncio import CancelledError

from aiogram import Dispatcher
from loguru import logger

from src import config
from src import di
from src.presentation.bots.admin_bot.bot import run as admin_bot_run
from src.presentation.bots.client_bot.bot import run as client_bot_run
from src.presentation.bots.employee_bot.bot import run as employee_bot_run
from src.presentation.user_state_storage import UserStateStorage


async def main():
    logger.remove()
    logger.add(sys.stdout)
    try:
        user_state_service = di.container.user_state_service()
        storage = UserStateStorage(user_state_service)
        await asyncio.gather(
            admin_bot_run(token=config.ADMIN_BOT_TOKEN, dp=Dispatcher(storage=storage)),
            client_bot_run(token=config.CLIENT_BOT_TOKEN, dp=Dispatcher(storage=storage)),
            employee_bot_run(token=config.EMPLOYEE_BOT_TOKEN, dp=Dispatcher(storage=storage)),
        )
    except CancelledError:
        await di.container.session_manager().disconnect()


if __name__ == '__main__':
    asyncio.run(main())
