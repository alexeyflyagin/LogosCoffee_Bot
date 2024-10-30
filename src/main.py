import asyncio
from asyncio import CancelledError

from src.bots.admin_bot import admin_bot
from src.bots.employee_bot import employee_bot
from src.bots.client_bot import client_bot


async def main():
    try:
        await asyncio.gather(
            admin_bot.start_bot(),
            employee_bot.start_bot(),
            client_bot.start_bot(),
        )
    except CancelledError:
        pass


if __name__ == '__main__':
    # migrations.upgrade_head()
    asyncio.run(main())
