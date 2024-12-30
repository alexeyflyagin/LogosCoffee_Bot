from datetime import datetime

from pydantic import TypeAdapter
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao import dao_product, dao_product_and_order, dao_order
from src.data.logoscoffee.dao.units import raise_exception_if_none
from src.data.logoscoffee.db.models import OrderOrm, ProductAndOrderOrm, ProductOrm
from src.data.logoscoffee.entities.enums import OrderState, OrderStateGroup
from src.data.logoscoffee.entities.general_entities import OrderPlaceAttemptEntity
from src.data.logoscoffee.entities.orm_entities import OrderEntity, ProductAndOrderEntity
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError, PlacedOrderIsEmptyError, \
    ProductIsNotAvailableError, \
    ProductMissingError, OrderNotFoundError
from src.data.logoscoffee.interfaces.client_order_service import ClientOrderService
from src.data.logoscoffee.session_manager import SessionManager


class ClientOrderServiceImpl(ClientOrderService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __safe_get_draft_order(self, s: AsyncSession, client_id: int, block_row: bool = False) -> OrderOrm:
        order = await dao_order.get_by_id(s, client_id, block_row)
        raise_exception_if_none(order, e=OrderNotFoundError(client_id=client_id))
        return order

    async def get_draft_order(self, client_id: int) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                order = await dao_order.get_one_by_client_id_and_state(s, client_id, OrderState.CREATED, join=True)
                entity = OrderEntity.model_validate(order)
                entity.product_and_orders_rs = []
                for i in order.product_and_orders:
                    product_and_order_entity = ProductAndOrderEntity.model_validate(i)
                    product_and_order_entity.product_rs = i.product
                    entity.product_and_orders_rs.append(product_and_order_entity)
                return entity
        # TODO ClientAccountNotFoundError handler
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def add_to_draft_order(self, client_id: int, product_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__safe_get_draft_order(s, client_id, True)
                product = await dao_product.get_by_id(s, product_id)
                if product.is_available:
                    product_and_order = ProductAndOrderOrm(order_id=order.id, product_id=product.id)
                    s.add(product_and_order)
                else:
                    products_and_orders = await dao_product_and_order.get(s, product_id=product.id, order_id=order.id)
                    for i in products_and_orders:
                        await s.delete(i)
                await s.commit()
        # TODO add ClientAccountNotFoundError handler
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def remove_from_draft_order(self, client_id: int, product_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__safe_get_draft_order(s, client_id, True)
                product = await dao_product.get_by_id(s, product_id)
                product_and_orders = await dao_product_and_order.get(s, product_id=product.id, order_id=order.id)
                if product.is_available:
                    product_and_order = product_and_orders[0] if product_and_orders else None
                    if not product_and_order:
                        raise ProductMissingError(order_id=order.id, product_id=product.id)
                    await s.delete(product_and_order)
                else:
                    for i in product_and_orders:
                        await s.delete(i)
                await s.commit()
        # TODO add ClientAccountNotFoundError handler
        except ProductMissingError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def clear_draft_order(self, client_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__safe_get_draft_order(s, client_id, True)
                products_and_order = await dao_product_and_order.get_by_order_id(s, order_id=order.id)
                for i in products_and_order:
                    await s.delete(i)
                await s.commit()
        # TODO add ClientAccountNotFoundError handler
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def place_order(self, client_id: int, order_id: int | None = None) -> OrderPlaceAttemptEntity:
        try:
            async with self.__session_manager.get_session() as s:
                if order_id:
                    order = await dao_order.get_by_id(s, _id=order_id, with_for_update=True)
                    if order is None:
                        raise OrderNotFoundError(order_id=order_id)
                else:
                    order = await self.__safe_get_draft_order(s, client_id, True)
                products_and_order = await dao_product_and_order.get_by_order_id(s, order_id=order.id, join=True)
                if len(products_and_order) == 0:
                    raise PlacedOrderIsEmptyError
                deleted_items = []
                for i in products_and_order:
                    if not i.product.is_available:
                        deleted_items.append(i)
                    else: i.product_price = i.product.price
                [await s.delete(i) for i in deleted_items]
                order.date_pending = datetime.now()
                await s.flush()
                order_entity = OrderEntity.model_validate(order)
                await s.commit()
                is_successful = len(deleted_items) == 0
                return OrderPlaceAttemptEntity(order=order_entity, is_successful=is_successful)
        except OrderNotFoundError as e:
            logger.error(e)
            raise
        # TODO add ClientAccountNotFoundError handler
        except (ProductIsNotAvailableError, PlacedOrderIsEmptyError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_in_progress_orders(self, client_id: int) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                orders = await dao_order.get_by_client_id_and_state_group(s, client_id, OrderStateGroup.IN_PROGRESS)
                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)
                return order_entities
        # TODO add ClientAccountNotFoundError handler
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_archived_orders(self, client_id: int) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                orders = await dao_order.get_by_client_id_and_state_group(s, client_id, OrderStateGroup.CLOSED)
                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)
                return order_entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_product_quantity_in_draft_order(self, client_id: int, product_id: int) -> int:
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__safe_get_draft_order(s, client_id, True)
                products = await dao_product_and_order.get(s, product_id=product_id, order_id=order.id)
                return len(products)
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
