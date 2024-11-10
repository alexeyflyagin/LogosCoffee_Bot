import asyncio
import sys

from loguru import logger

from src.di.container import di


async def main():
    logger.remove()
    logger.add(sys.stdout)
    try:
        await asyncio.gather(
            di.admin_bot().run(),
            di.client_bot().run(),
            di.employee_bot().run(),
        )
    finally:
        await di.session_manager().disconnect()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
