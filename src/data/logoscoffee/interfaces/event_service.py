from abc import ABC, abstractmethod

from src.data.logoscoffee.entities.orm_entities import EventSubscriberEntity


class EventService(ABC):

    @abstractmethod
    async def get_subscribers(self, event_name: str) -> list[EventSubscriberEntity]:
        pass

    @abstractmethod
    async def subscribe(self, event_name: str, chat_id: int):
        pass

    @abstractmethod
    async def unsubscribe(self, event_name: str, chat_id: int):
        pass
