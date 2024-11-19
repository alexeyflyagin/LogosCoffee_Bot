from enum import Enum

from src import config


class FileAddress:
    SEPARATOR = ":::"

    class BotType(Enum):
        ADMIN_BOT = config.ADMIN_BOT_TOKEN
        EMPLOYEE_BOT = config.EMPLOYEE_BOT_TOKEN
        CLIENT_BOT = config.CLIENT_BOT_TOKEN

    def __init__(self, bot_type: BotType, file_id: str):
        self.bot_type = bot_type
        self.file_id = file_id

    @property
    def address(self) -> str:
        return self.bot_type.name + FileAddress.SEPARATOR + self.file_id

    @staticmethod
    def from_address(address: str) -> "FileAddress":
        res = address.split(FileAddress.SEPARATOR)
        if len(res) != 2:
            raise ValueError(f"The address ({address}) is incorrect.")
        return FileAddress(FileAddress.BotType.__getitem__(res[0]), file_id=res[1])
