from dataclasses import dataclass
from src.data.services.logos_coffee_service.database import database

from sqlalchemy.ext.asyncio import AsyncSession

@dataclass
class UserData:
    bot_id: int
    user_id: int
    chat_id: int

# async def __get_user_state_or_create(s:AsyncSession,    ):


async def set_state(user_data: UserData, state: str | None):
    pass

async def get_state(user_data: UserData) -> str | None:
    pass

async def set_data(user_data: UserData, data: dict):
    pass

async def get_data(user_data: UserData) -> dict:
    pass
