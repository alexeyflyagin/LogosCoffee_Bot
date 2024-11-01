import asyncio
import sys
from asyncio import CancelledError

from loguru import logger
from bots.admin_bot import admin_bot
from bots.employee_bot import employee_bot
from bots.client_bot import client_bot
from data.services.database import database

async def main():
    logger.remove()
    logger.add(sys.stdout)
    try:
        await asyncio.gather(
            admin_bot.start_bot(),
            employee_bot.start_bot(),
            client_bot.start_bot(),
        )
    except CancelledError:
        await database.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
