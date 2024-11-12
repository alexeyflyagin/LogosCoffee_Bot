class FileAddress:
    SEPARATOR = ":::"

    def __init__(self, bot_token: str, file_id: str):
        self.bot_token = bot_token
        self.file_id = file_id

    @property
    def address(self) -> str:
        return self.bot_token + FileAddress.SEPARATOR + self.file_id

    @staticmethod
    def from_address(address: str) -> "FileAddress":
        res = address.split(FileAddress.SEPARATOR)
        if len(res) != 2:
            raise ValueError(f"The address ({address}) is incorrect.")
        return FileAddress(bot_token=res[0], file_id=res[1])
