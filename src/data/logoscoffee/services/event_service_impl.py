from datetime import datetime
from typing import Any

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.db.models import EventSubscriberOrm
from src.data.logoscoffee.entities.orm_entities import EventSubscriberEntity
from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, AlreadySubscribedError, \
    AlreadyUnsubscribedError
from src.data.logoscoffee.interfaces.event_service import EventService
from src.data.logoscoffee.session_manager import SessionManager


class EventServiceImpl(EventService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def get_subscribers(self, event_name: str) -> list[EventSubscriberEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(EventSubscriberOrm).filter(EventSubscriberOrm.event_name == event_name))
                subscribers = res.scalars().all()
                entities = [EventSubscriberEntity.model_validate(i) for i in subscribers]
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def subscribe(self, event_name: str, chat_id: int, data: dict[str, Any] = None):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(EventSubscriberOrm).filter(EventSubscriberOrm.event_name == event_name,
                                                                        EventSubscriberOrm.chat_id == chat_id))
                subscriber = res.scalars().first()
                if subscriber:
                    raise AlreadySubscribedError(chat_id, event_name)
                new_subscriber = EventSubscriberOrm(event_name=event_name, chat_id=chat_id, data=data)
                s.add(new_subscriber)
                await s.commit()
        except AlreadySubscribedError as e:
            await s.rollback()
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)

    async def unsubscribe(self, event_name: str, chat_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(EventSubscriberOrm).filter(EventSubscriberOrm.event_name == event_name,
                                                                        EventSubscriberOrm.chat_id == chat_id))
                subscriber = res.scalars().first()
                if not subscriber:
                    raise AlreadyUnsubscribedError(chat_id, event_name)
                await s.delete(subscriber)
                await s.commit()
        except AlreadyUnsubscribedError as e:
            await s.rollback()
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)