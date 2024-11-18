from loguru import logger

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity, OrderEntity
from src.data.logoscoffee.interfaces.employee_service import EmployeeService
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.db.models import EmployeeAccountOrm, OrderOrm
from src.data.logoscoffee.session_manager import SessionManager


class EmployeeServiceImpl(EmployeeService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def login(self, key: str | None) -> EmployeeAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                query = await s.execute(select(EmployeeAccountOrm).filter(EmployeeAccountOrm.key == key))
                account = query.scalars().first()
                if account is None:
                    raise InvalidKey(key)
                return EmployeeAccountEntity.model_validate(account)
        except InvalidKey as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_new_orders(self, last_update_time: datetime) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(OrderOrm).filter(OrderOrm.date_pending >= last_update_time))
                orders = res.scalars().all()

                adapter = TypeAdapter(list[OrderEntity])
                entities = adapter.validate_python(orders)

                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def accept_order(self, order_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(OrderOrm).filter(OrderOrm.id == order_id))
                order = res.scalars().first()

                order.date_pending = datetime.now()
                await s.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def cancel_order(self, order_id: int, cancel_details: str):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(OrderOrm).filter(OrderOrm.id == order_id))
                order = res.scalars().first()

                order.date_canceled = datetime.now()
                order.cancel_details = cancel_details
                await s.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def start_cook_order(self, order_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(OrderOrm).filter(OrderOrm.id == order_id))
                order = res.scalars().first()

                order.date_cooking = datetime.now()
                await s.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def ready_order(self, order_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(OrderOrm).filter(OrderOrm.id == order_id))
                order = res.scalars().first()

                order.date_ready = datetime.now()
                await s.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def complete_order(self, order_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(OrderOrm).filter(OrderOrm.id == order_id))
                order = res.scalars().first()

                order.date_completed = datetime.now()
                await s.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
