from loguru import logger

from pydantic import TypeAdapter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_order, dao_employee_account
from src.data.logoscoffee.entities.enums import OrderState
from src.data.logoscoffee.entities.orm_entities import EmployeeAccountEntity, OrderEntity
from src.data.logoscoffee.interfaces.employee_service import EmployeeService
from src.data.logoscoffee.exceptions import *
from src.data.logoscoffee.db.models import OrderOrm
from src.data.logoscoffee.services.units import create_draft_orm
from src.data.logoscoffee.session_manager import SessionManager


class EmployeeServiceImpl(EmployeeService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __get_order_by_id(self, s: AsyncSession, order_id) -> OrderOrm:
        order = await dao_order.get_by_id(s, order_id, with_for_update=True)
        return order

    def __check_state(self, order: OrderOrm, expected_state: OrderState):
        order_entity = OrderEntity.model_validate(order)
        if order_entity.state != expected_state:
            raise OrderStateError(state=order_entity.state, expected_state=expected_state)
        if (order_entity.state == OrderState.CANCELED or
            order_entity.state == OrderState.COMPLETED):
            return
        for i in range(1, expected_state.value):
            state = OrderState(i)
            if state == OrderState.PENDING and not order_entity.date_pending:
                raise OrderStateError(state=state, expected_state=expected_state)
            if state == OrderState.COOKING and not order_entity.date_cooking:
                raise OrderStateError(state=state, expected_state=expected_state)
            if state == OrderState.READY and not order_entity.date_ready:
                raise OrderStateError(state=state, expected_state=expected_state)

    def __check_order_is_not_finished(self, order: OrderOrm):
        order_entity = OrderEntity.model_validate(order)
        if order_entity.state == OrderState.CANCELED or order_entity.state == OrderState.COMPLETED:
            raise OrderStateError(state=order_entity.state, expected_state="Is not Canceled or Completed")

    async def get_new_orders(self, last_update: datetime) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                orders = await dao_order.get_since_by_date_pending(s, last_update)
                adapter = TypeAdapter(list[OrderEntity])
                entities = adapter.validate_python(orders)
                return entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def login(self, key: str | None) -> EmployeeAccountEntity:
        try:
            async with self.__session_manager.get_session() as s:
                account = await dao_employee_account.get_by_key(s, key)
                if account is None:
                    raise InvalidKeyError(key)
                return EmployeeAccountEntity.model_validate(account)
        except InvalidKeyError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def accept_order(self, order_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_order_by_id(s, order_id)
                self.__check_state(order, OrderState.PENDING)

                order.date_cooking = datetime.now()
                await create_draft_orm(s, order.client_id)
                await s.commit()
        except OrderStateError as e:
            logger.error(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def cancel_order(self, order_id: int, cancel_details: str):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_order_by_id(s, order_id)
                self.__check_order_is_not_finished(order)

                order.date_canceled = datetime.now()
                order.cancel_details = cancel_details
                await s.commit()
        except OrderStateError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def ready_order(self, order_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_order_by_id(s, order_id)
                self.__check_state(order, OrderState.COOKING)

                order.date_ready = datetime.now()
                await s.commit()
        except OrderStateError as e:
            logger.error(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def complete_order(self, order_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_order_by_id(s, order_id)
                self.__check_state(order, OrderState.READY)

                order.date_completed = datetime.now()
                await s.commit()
        except OrderStateError as e:
            logger.error(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
