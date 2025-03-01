from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_order, dao_client_account
from src.data.logoscoffee.db.models import OrderOrm
from src.data.logoscoffee.entities.orm_entities import OrderEntity, ClientAccountEntity
from src.data.logoscoffee.enums import OrderStateGroup, OrderState
from src.data.logoscoffee.exceptions import DatabaseError, InvalidTokenError, OrderStateError, LCError, \
    OrderNotFoundError
from src.data.logoscoffee.interfaces.employee_order_service import EmployeeOrderService
from src.data.logoscoffee.models import CancelOrderData
from src.data.logoscoffee.services.utils import get_employee_account_by_token, generate_pickup_code, \
    raise_exception_if_none
from src.data.logoscoffee.session_manager import SessionManager
from src.loggers import service_logger as logger


class EmployeeOrderServiceImpl(EmployeeOrderService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __next_order_state(self, session: AsyncSession, order: OrderOrm):
        entity = OrderEntity.model_validate(order)
        if entity.state == OrderState.PENDING:
            order.date_cooking = datetime.now()
        elif entity.state == OrderState.COOKING:
            order.date_ready = datetime.now()
            order.pickup_code = await generate_pickup_code(session)
        elif entity.state == OrderState.READY:
            order.date_completed = datetime.now()
            order.pickup_code = None
        else:
            raise OrderStateError(msg=f"Incorrect state of order (id={order.id}, state={entity.state.name})")

    async def next_order_state(
            self,
            token: str,
            order_id: int,
    ) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                await get_employee_account_by_token(s, token)
                order = await dao_order.get_by_id(s, order_id, with_for_update=True)
                raise_exception_if_none(order, OrderNotFoundError(id=order_id))
                await self.__next_order_state(s, order)
                await s.flush()
                client = await dao_client_account.get_by_id(s, order.client_id)
                order_entity = OrderEntity.model_validate(order)
                order_entity.client = ClientAccountEntity.model_validate(client)
                await s.commit()
                return order_entity
        except (InvalidTokenError, OrderStateError, OrderNotFoundError) as e:
            logger.debug(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise LCError(f"Occurred an unexpected error: {e}")

    async def cancel_order(self, token: str, order_id: int, data: CancelOrderData) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                await get_employee_account_by_token(s, token)
                order = await dao_order.get_by_id(s, order_id, with_for_update=True)
                raise_exception_if_none(order, OrderNotFoundError(id=order_id))
                order_entity = OrderEntity.model_validate(order)
                if order_entity.state_group == OrderStateGroup.CLOSED:
                    raise OrderStateError(msg=f"The Order (id={order_id}) has state_group 'CLOSED'")
                order.date_canceled = datetime.now()
                order.cancel_details = data.details
                order.pickup_code = None
                await s.flush()
                client = await dao_client_account.get_by_id(s, order.client_id)
                order_entity = OrderEntity.model_validate(order)
                order_entity.client = ClientAccountEntity.model_validate(client)
                await s.commit()
                return order_entity
        except (InvalidTokenError, OrderStateError, OrderNotFoundError) as e:
            logger.debug(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise LCError(f"Occurred an unexpected error: {e}")

    async def get_order_by_id(self, token: str, order_id: int) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                await get_employee_account_by_token(s, token)
                order = await dao_order.get_by_id(s, order_id, with_for_update=True)
                raise_exception_if_none(order, OrderNotFoundError(id=order_id))
                client = await dao_client_account.get_by_id(s, order.client_id)
                order_entity = OrderEntity.model_validate(order)
                order_entity.client = ClientAccountEntity.model_validate(client)
                await s.commit()
                return order_entity
        except (InvalidTokenError, OrderNotFoundError) as e:
            logger.debug(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise LCError(f"Occurred an unexpected error: {e}")
