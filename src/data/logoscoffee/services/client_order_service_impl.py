from datetime import datetime

from pydantic import TypeAdapter
from loguru import logger
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.data.logoscoffee.db.models import OrderOrm, ProductAndOrderOrm, ProductOrm
from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError, PlacedOrderIsEmpty, ProductIsNotAvailable
from src.data.logoscoffee.interfaces.client_order_service import ClientOrderService
from src.data.logoscoffee.session_manager import SessionManager


class ClientOrderServiceImpl(ClientOrderService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __get_draft_order(self, s: AsyncSession, client_id: int, block_row: bool = False) -> OrderOrm:
        if block_row:
            res = await s.execute(select(OrderOrm).filter(
            OrderOrm.client_id == client_id, OrderOrm.date_pending is None).with_for_update())
        else: res = await s.execute(select(OrderOrm).filter(
            OrderOrm.client_id == client_id, OrderOrm.date_pending is None))
        order = res.scalars().first()
        return order

    async def __get_product(self, s: AsyncSession, product_id: int) -> ProductOrm:
        res = await s.execute(select(ProductOrm).filter(ProductOrm.id == product_id))
        product = res.scalars().first()
        return product

    async def get_draft_order(self, client_id: int) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_draft_order(s, client_id)
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
                order = await self.__get_draft_order(s, client_id, True)
                product = await self.__get_product(s, product_id)
                if not product.is_available:
                    raise ProductIsNotAvailable(id=product.id)
                product_and_order = ProductAndOrderOrm(order_id=order.id, product_id=product.id)
                s.add(product_and_order)
                await s.commit()
        except ProductIsNotAvailable as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def remove_from_draft_order(self, client_id: int, product_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_draft_order(s, client_id, True)
                product = await self.__get_product(s, product_id)
                res_product_and_order = await s.execute(select(ProductAndOrderOrm).filter(
                    ProductAndOrderOrm.order_id == order.id, ProductAndOrderOrm.product_id == product.id))
                product_and_order = res_product_and_order.scalars().first()

                await s.delete(product_and_order)
                await s.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def clear_draft_order(self, client_id: int):
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_draft_order(s, client_id, True)
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
                order = await self.__get_draft_order(s, client_id, True)
                res_products_and_order = await s.execute(select(ProductAndOrderOrm).filter(ProductAndOrderOrm.order_id == order.id)
                                                         .options(joinedload(ProductAndOrderOrm.product)))
                products_and_order = res_products_and_order.unique().scalars().all()
                if len(products_and_order) == 0:
                    raise PlacedOrderIsEmpty
                for i in products_and_order:
                    if not i.product.is_available:
                        raise ProductIsNotAvailable
                order.date_pending = datetime.now()
                await s.flush()
                order_entity = OrderEntity.model_validate(order)
                await s.commit()
                return order_entity
        except ProductIsNotAvailable as e:
            logger.warning(e)
            raise
        except PlacedOrderIsEmpty as e:
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

    async def get_in_progress_orders(self, client_id: int) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                res_order = await s.execute(select(OrderOrm).filter(
                    OrderOrm.client_id == client_id, OrderOrm.date_pending is not None,
                    OrderOrm.date_canceled is None, OrderOrm.date_completed is None))
                orders = res_order.scalars().all()

                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)

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
                res_orders = await s.execute(select(OrderOrm).filter(
                    or_(OrderOrm.client_id == client_id, OrderOrm.date_canceled is not None,
                        OrderOrm.client_id == client_id, OrderOrm.date_completed is not None)))
                orders = res_orders.scalars().all()

                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)

                return order_entities
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_products_in_client_order_count(self, client_id: int, product_id: int) -> int:
        try:
            async with self.__session_manager.get_session() as s:
                order = await self.__get_draft_order(s, client_id, True)
                res_products = await s.execute(select(ProductAndOrderOrm).filter(
                    ProductAndOrderOrm.product_id == product_id,
                    ProductAndOrderOrm.order_id == order.id))
                products = res_products.scalars().all()

                return len(products)
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
