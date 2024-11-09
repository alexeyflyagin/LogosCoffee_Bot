from abc import ABC, abstractmethod

from aiogram import Bot, Dispatcher


class BaseBot(ABC):

    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp

    @abstractmethod
    async def run(self):
        pass