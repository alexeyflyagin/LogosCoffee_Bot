from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.event_entities import EventSubscriberEntity


class EventService(ABC):

    @abstractmethod
    async def get_subscribers(self, event_name: str) -> list[EventSubscriberEntity]:
        pass

    @abstractmethod
    async def subscribe(self, event_name: str, user_state_id: int):
        pass

    @abstractmethod
    async def unsubscribe(self, event_name: str, user_state_id: int):
        pass

    @abstractmethod
    async def get_user_state_id(self, bot_id: int, user_id: int, chat_id: int) -> int:
        pass
