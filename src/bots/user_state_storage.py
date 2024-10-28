from typing import Dict, Any, Optional

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from src.data.services.logos_coffee_service import user_state_service as service
from src.data.services.logos_coffee_service.database import database
from src.data.services.logos_coffee_service.user_state_service import UserData


def get_user_data_from_key_storage(key: StorageKey):
    return UserData(key.bot_id, key.user_id, key.chat_id)

class UserStateStorage(BaseStorage):

    async def set_state(self, key: StorageKey, state: StateType = None):
        user_data = get_user_data_from_key_storage(key)
        str_state = state.state if state else None
        await service.set_state(user_data, str_state)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        user_data = get_user_data_from_key_storage(key)
        res = await service.get_state(user_data)
        return res

    async def set_data(self, key: StorageKey, data: Dict[str, Any]):
        user_data = get_user_data_from_key_storage(key)
        await service.set_data(user_data, data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        user_data = get_user_data_from_key_storage(key)
        res = await service.get_data(user_data)
        return res

    async def close(self) -> None:
        await database.disconnect()


storage = UserStateStorage()
