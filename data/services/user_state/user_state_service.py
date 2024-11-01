from dataclasses import dataclass
from data.services.database import database
from data.services.models import UserStateOrm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

@dataclass
class UserData:
    bot_id: int
    user_id: int
    chat_id: int

async def __create_user_state(s:AsyncSession, user_data: UserData) -> UserStateOrm:
    user_state = UserStateOrm(bot_id = user_data.bot_id, user_id = user_data.user_id, chat_id = user_data.chat_id,
                              state = None, data = dict())
    s.add(user_state)
    return user_state

async def __get_user_state_or_create(s:AsyncSession, user_data: UserData) -> UserStateOrm:
    where = ((UserStateOrm.user_id == user_data.user_id), (UserStateOrm.bot_id == user_data.bot_id),
             (UserStateOrm.chat_id == user_data.chat_id))
    res = await s.execute(select(UserStateOrm).filter(*where))
    user_state = res.scalar_one_or_none()
    if not user_state:
        await __create_user_state(s, user_data)
        res = await s.execute(select(UserStateOrm).filter(*where))
        user_state = res.scalar_one_or_none()
    return user_state

async def set_state(user_data: UserData, state: str | None):
    async with database.session_factory() as session:
        user_state = await __get_user_state_or_create(session, user_data)
        user_state.state = state
        await session.commit()

async def get_state(user_data: UserData) -> str | None:
    async with database.session_factory() as session:
        user_state = await __get_user_state_or_create(session, user_data)
        return user_state.state

async def set_data(user_data: UserData, data: dict):
    async with database.session_factory() as session:
        user_state = await __get_user_state_or_create(session, user_data)
        user_state.data = data
        await session.commit()

async def get_data(user_data: UserData) -> dict:
    async with database.session_factory() as session:
        user_state = await __get_user_state_or_create(session, user_data)
        return user_state.data
