from typing import Dict, Any, Optional

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from src.data.logoscoffee.interfaces.user_state_service import UserData, UserStateService


def get_user_data_from_key_storage(key: StorageKey):
    return UserData(key.bot_id, key.user_id, key.chat_id)

class UserStateStorage(BaseStorage):

    def __init__(self, user_state_service: UserStateService):
        self.service = user_state_service

    async def set_state(self, key: StorageKey, state: StateType = None):
        user_data = get_user_data_from_key_storage(key)
        str_state = state.state if state else None
        await self.service.set_state(user_data, str_state)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        user_data = get_user_data_from_key_storage(key)
        res = await self.service.get_state(user_data)
        return res

    async def set_data(self, key: StorageKey, data: Dict[str, Any]):
        user_data = get_user_data_from_key_storage(key)
        await self.service.set_data(user_data, data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        user_data = get_user_data_from_key_storage(key)
        res = await self.service.get_data(user_data)
        return res

    async def close(self) -> None:
        pass
