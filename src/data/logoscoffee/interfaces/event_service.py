from abc import ABC, abstractmethod
from typing import Any

from src.data.logoscoffee.entities.orm_entities import EventSubscriberEntity


class EventService(ABC):

    @abstractmethod
    async def get_subscribers(
            self,
            event_name: str
    ) -> list[EventSubscriberEntity]:
        """
        :param event_name: The tag that listeners will use to subscribe.
        :return: The list of subscribers to an event with the tag `event_name`
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def subscribe(
            self,
            event_name: str,
            chat_id: int,
            data: dict[str, Any] = None
    ):
        """
        :param event_name: The event tag that the subscriber will listen to
        :param chat_id: The ID of the subscriber chat
        :param data: The dict for additional information (eg: message id)
        :raises AlreadySubscribedError: If a subscriber with `chat_id` has already been added
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass

    @abstractmethod
    async def unsubscribe(
            self,
            event_name: str,
            chat_id: int
    ):
        """
        :param event_name: The event tag that the subscriber is listening to
        :param chat_id: The ID of the subscriber chat
        :raises AlreadyUnsubscribedError: If a subscriber with `chat_id` has already been removed
        :raises DatabaseError:
        :raises UnknownError:
        """
        pass
