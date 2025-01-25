from abc import ABC, abstractmethod

from aiogram import Bot, Dispatcher
from src.loggers import bot_logger as logger


class BaseBot(ABC):

    def __init__(self, bot: Bot, dp: Dispatcher, name: str = "No name"):
        self.bot = bot
        self.dp = dp
        self.name = name
        self.dp.startup.register(self.startup)

    def startup(self):
        logger.info(f"{self.name} bot is started.")

    def shutdown(self):
        logger.info(f"{self.name} bot is finished.")

    @abstractmethod
    async def run(self):
        pass