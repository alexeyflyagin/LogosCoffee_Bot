from datetime import datetime

from pydantic import TypeAdapter
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.db.models import OrderOrm, ProductAndOrderOrm, ProductOrm
from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError, PlacedOrderIsEmpty
from src.data.logoscoffee.interfaces.client_order_service import ClientOrderService
from src.data.logoscoffee.session_manager import SessionManager


class ClientOrderServiceImpl(ClientOrderService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def get_draft_order(self, client_id: int) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                res = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_pending is None))
                order = res.scalars().first()
                #if order is None: ToDo нужно ли рассматривать такой случай?
                entity = OrderEntity.model_validate(order)
                return entity
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def add_to_draft_order(self, client_id: int, product_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res_order = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_pending is None))
                order = res_order.scalars().first()
                res_product = await s.execute(select(ProductOrm).filter(ProductOrm.id == product_id))
                product = res_product.scalars().first()

                product_and_order = ProductAndOrderOrm(order_id=order.id, product_id=product.id)
                s.add(product_and_order)
                await s.commit()
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)

    async def remove_from_draft_order(self, client_id: int, product_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res_order = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_pending is None))
                order = res_order.scalars().first()
                res_product = await s.execute(select(ProductOrm).filter(ProductOrm.id == product_id))
                product = res_product.scalars().first()
                res_product_and_order = await s.execute(select(ProductAndOrderOrm).filter(
                    ProductAndOrderOrm.order_id == order.id, ProductAndOrderOrm.product_id == product_id))
                product_and_order = res_product_and_order.scalars().first()

                await s.delete(product_and_order)
                await s.commit()
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)

    async def clear_draft_order(self, client_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                res_order = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_pending is None))
                order = res_order.scalars().first()
                res_product_and_order = await s.execute(select(ProductAndOrderOrm).filter(
                    ProductAndOrderOrm.order_id == order.id))
                products_and_order = res_product_and_order.scalars().all()

                for i in products_and_order:
                    await s.delete(i)
                await s.commit()
        except SQLAlchemyError as e:
            await s.rollback()
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            await s.rollback()
            logger.exception(e)
            raise UnknownError(e)


    async def place_order(self, client_id: int, order_id: int) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                res_order = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_pending is None))
                order = res_order.scalars().first()
                order.date_pending = datetime.now()
                await s.flush()
                order_entity = OrderEntity.model_validate(order)
                await s.commit()
                return order_entity
        except PlacedOrderIsEmpty as e:
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

    async def get_current_orders(self, client_id: int) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                res_order = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_pending is None))
                orders = res_order.scalars().all()

                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)

                await s.commit()
                return order_entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_archived_orders(self, client_id: int) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                res_order_canceled = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_canceled is not None))
                res_order_completed = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_completed is not None))
                orders_canceled = res_order_canceled.scalars().all()
                orders_completed = res_order_completed.scalars().all()
                orders = list(orders_canceled) + list(orders_completed)

                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)

                await s.commit()
                return order_entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
