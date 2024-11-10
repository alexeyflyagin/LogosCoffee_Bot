from datetime import datetime

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.data.logoscoffee.db.models import EventSubscriberOrm, UserStateOrm
from src.data.logoscoffee.entities.orm_entities import EventSubscriberEntity, UserStateEntity
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
                res = await s.execute(select(EventSubscriberOrm).options(joinedload(EventSubscriberOrm.user_state))
                                      .filter(EventSubscriberOrm.event_name == event_name))
                subscribers = res.unique().scalars().all()
                entities = []
                for i in subscribers:
                    user_state_entity = UserStateEntity.model_validate(i.user_state)
                    entity = EventSubscriberEntity(i.id, i.event_name, i.date_create, i.user_state_id, user_state_entity)
                    entities.append(entity)
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def subscribe(self, event_name: str, user_state_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(EventSubscriberOrm).filter(EventSubscriberOrm.event_name == event_name,
                                                                        EventSubscriberOrm.user_state_id == user_state_id))
                subscriber = res.scalars().first()
                if subscriber:
                    raise AlreadySubscribedError(user_state_id, event_name)
                new_subscriber = EventSubscriberOrm(event_name=event_name, date_create=datetime.now(),
                                                    user_state_id=user_state_id)
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

    async def unsubscribe(self, event_name: str, user_state_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(EventSubscriberOrm).filter(EventSubscriberOrm.event_name == event_name,
                                                                        EventSubscriberOrm.user_state_id == user_state_id))
                subscriber = res.scalars().first()
                if not subscriber:
                    raise AlreadyUnsubscribedError(user_state_id, event_name)
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

    async def get_user_state_id(self, bot_id: int, user_id: int, chat_id: int) -> int:
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(UserStateOrm).filter(UserStateOrm.user_id == user_id,
                                                                  UserStateOrm.bot_id == bot_id,
                                                                  UserStateOrm.chat_id == chat_id))
                user_state = res.scalars().first()
                return user_state.id
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)