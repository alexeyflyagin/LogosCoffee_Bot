from dataclasses import dataclass


@dataclass
class UserData:
    bot_id: int
    user_id: int
    chat_id: int
