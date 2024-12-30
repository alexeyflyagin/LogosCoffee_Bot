from typing import Any

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.dao import dao_event_subscriber
from src.data.logoscoffee.db.models import EventSubscriberOrm
from src.data.logoscoffee.entities.orm_entities import EventSubscriberEntity
from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, AlreadySubscribedError, \
    AlreadyUnsubscribedError
from src.data.logoscoffee.interfaces.event_service import EventService
from src.data.logoscoffee.session_manager import SessionManager


class EventServiceImpl(EventService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def get_subscribers(
            self,
            event_name: str
    ) -> list[EventSubscriberEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                subscribers = await dao_event_subscriber.get_by_event_name(s, event_name)
                entities = [EventSubscriberEntity.model_validate(i) for i in subscribers]
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def subscribe(
            self,
            event_name: str,
            chat_id: int,
            data: dict[str, Any] = None
    ):
        try:
            async with self.__session_manager.get_session() as s:
                subscriber = await dao_event_subscriber.get(s, event_name, chat_id)
                if subscriber:
                    raise AlreadySubscribedError(chat_id, event_name)
                new_subscriber = EventSubscriberOrm(event_name=event_name, chat_id=chat_id, data=data)
                s.add(new_subscriber)
                await s.commit()
        except AlreadySubscribedError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def unsubscribe(
            self,
            event_name: str,
            chat_id: int
    ):
        try:
            async with self.__session_manager.get_session() as s:
                subscriber = await dao_event_subscriber.get(s, event_name, chat_id)
                if not subscriber:
                    raise AlreadyUnsubscribedError(chat_id, event_name)
                await s.delete(subscriber)
                await s.commit()
        except AlreadyUnsubscribedError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)