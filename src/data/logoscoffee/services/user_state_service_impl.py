from src.data.logoscoffee.entities.user_state_entities import UserData
from src.data.logoscoffee.interfaces.user_state_service import UserStateService
from src.data.logoscoffee.db.models import UserStateOrm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.data.logoscoffee.session_manager import SessionManager


class UserStateServiceImpl(UserStateService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager


    async def __create_user_state(self, s: AsyncSession, user_data: UserData) -> UserStateOrm:
        user_state = UserStateOrm(bot_id=user_data.bot_id, user_id=user_data.user_id, chat_id=user_data.chat_id,
                                  state=None, data=dict())
        s.add(user_state)
        return user_state

    async def __get_user_state_or_create(self, s: AsyncSession, user_data: UserData) -> UserStateOrm:
        where = ((UserStateOrm.user_id == user_data.user_id), (UserStateOrm.bot_id == user_data.bot_id),
                 (UserStateOrm.chat_id == user_data.chat_id))
        res = await s.execute(select(UserStateOrm).filter(*where))
        user_state = res.scalar_one_or_none()
        if not user_state:
            await self.__create_user_state(s, user_data)
            res = await s.execute(select(UserStateOrm).filter(*where))
            user_state = res.scalar_one_or_none()
        return user_state


    async def set_state(self, user_data: UserData, state: str | None):
        async with self.__session_manager.get_session() as s:
            user_state = await self.__get_user_state_or_create(s, user_data)
            user_state.state = state
            await s.commit()

    async def get_state(self, user_data: UserData) -> str | None:
        async with self.__session_manager.get_session() as s:
            user_state = await self.__get_user_state_or_create(s, user_data)
            return user_state.state

    async def set_data(self, user_data: UserData, data: dict):
        async with self.__session_manager.get_session() as s:
            user_state = await self.__get_user_state_or_create(s, user_data)
            user_state.data = data
            await s.commit()

    async def get_data(self, user_data: UserData) -> dict:
        async with self.__session_manager.get_session() as s:
            user_state = await self.__get_user_state_or_create(s, user_data)
            return user_state.data
