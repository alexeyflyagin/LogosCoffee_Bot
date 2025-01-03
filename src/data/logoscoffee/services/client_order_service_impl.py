from datetime import datetime

from pydantic import TypeAdapter
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from src.data.logoscoffee.dao import dao_product, dao_product_and_order, dao_order
from src.data.logoscoffee.dao.units import raise_exception_if_none
from src.data.logoscoffee.db.models import ProductAndOrderOrm, ProductOrm
from src.data.logoscoffee.entities.enums import OrderStateGroup
from src.data.logoscoffee.entities.orm_entities import OrderEntity
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError, PlacedOrderIsEmptyError, \
    ProductIsNotAvailableError, OrderNotFoundError, InvalidTokenError, ProductNotFoundError
from src.data.logoscoffee.interfaces.client_order_service import ClientOrderService
from src.data.logoscoffee.services.units import safe_get_product_by_id, get_client_account_by_token, \
    get_draft_order_by_client_id
from src.data.logoscoffee.session_manager import SessionManager


class ClientOrderServiceImpl(ClientOrderService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    @staticmethod
    def __check_available_product_in_order(products: list[ProductOrm]):
        for product in products:
            if not product.is_available:
                continue
            raise ProductIsNotAvailableError(id=product.id)

    @staticmethod
    def __fix_prices(product_and_orders: tuple[ProductAndOrderOrm, ...]):
        for i in product_and_orders:
            i.product_price = i.product.price

    async def get_draft_order(
            self,
            token: str
    ) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                draft_order = await get_draft_order_by_client_id(s, account.id, join=True)
                entity = OrderEntity.model_validate(draft_order).set_relationships(draft_order)
                return entity
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def add_to_draft_order(
            self,
            token: str,
            product_id: int
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                draft_order = await get_draft_order_by_client_id(s, account.id)
                product = await safe_get_product_by_id(s, product_id)
                if not product.is_available:
                    product_and_orders = await dao_product_and_order.get(s, product_id, draft_order.id)
                    for i in product_and_orders:
                        await s.delete(i)
                    await s.commit()
                    raise ProductIsNotAvailableError(id=product_id)
                product_and_order = ProductAndOrderOrm(order_id=draft_order.id, product_id=product.id)
                s.add(product_and_order)
                draft_order_id = draft_order.id
                await s.commit()
                logger.success(f"The product (id={product_id}) added to the order (id={draft_order_id})")
        except (InvalidTokenError, ProductNotFoundError, ProductIsNotAvailableError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def remove_from_draft_order(
            self,
            token: str,
            product_id: int
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                draft_order = await get_draft_order_by_client_id(s, account.id)
                product = await dao_product.get_by_id(s, product_id)
                product_and_orders = await dao_product_and_order.get(s, product_id, draft_order.id)
                if not product.is_available:
                    for i in product_and_orders:
                        await s.delete(i)
                    await s.commit()
                    raise ProductIsNotAvailableError(id=product_id)
                if product_and_orders:
                    product_and_order = product_and_orders[0]
                    await s.delete(product_and_order)
                draft_order_id = draft_order.id
                await s.commit()
                logger.success(f"The product (id={product_id}) removed from the order (id={draft_order_id})")
        except (InvalidTokenError, ProductNotFoundError, ProductIsNotAvailableError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def clear_draft_order(
            self,
            token: str
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                draft_order = await get_draft_order_by_client_id(s, account.id)
                product_and_orders = await dao_product_and_order.get_by_order_id(s, draft_order.id)
                for i in product_and_orders:
                    await s.delete(i)
                draft_order_id = draft_order.id
                await s.commit()
                logger.success(f"All of the product removed from the order (id={draft_order_id})")
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def place_order(
            self,
            token: str,
            order_id: int | None = None
    ) -> OrderEntity:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                if not order_id:
                    draft_order = await get_draft_order_by_client_id(s, account.id)
                    order_id = draft_order.id
                order = await dao_order.get_by_id(s, order_id, with_for_update=True)
                raise_exception_if_none(order, OrderNotFoundError(order_id=order_id))
                product_and_orders = await dao_product_and_order.get_by_order_id(s, order_id, join=True)
                if len(product_and_orders) == 0:
                    raise PlacedOrderIsEmptyError
                self.__check_available_product_in_order([i.product for i in product_and_orders])
                self.__fix_prices(product_and_orders)
                order.date_pending = datetime.now()
                await s.flush()
                order_entity = OrderEntity.model_validate(order)
                await s.commit()
                logger.success(f"The order (id={order_id}) has been placed")
                return order_entity
        except (InvalidTokenError, ProductIsNotAvailableError, PlacedOrderIsEmptyError, OrderNotFoundError) as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_in_progress_orders(
            self,
            token: str
    ) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                orders = await dao_order.get_by_client_id_and_state_group(s, account.id, OrderStateGroup.IN_PROGRESS)
                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)
                return order_entities
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_closed_orders(
            self,
            token: str
    ) -> list[OrderEntity]:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                orders = await dao_order.get_by_client_id_and_state_group(s, account.id, OrderStateGroup.CLOSED)
                adapter = TypeAdapter(list[OrderEntity])
                order_entities = adapter.validate_python(orders)
                return order_entities
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)

    async def get_product_quantity_in_draft_order(
            self,
            token: str,
            product_id: int
    ) -> int:
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                order = await get_draft_order_by_client_id(s, account.id)
                products = await dao_product_and_order.get(s, product_id=product_id, order_id=order.id)
                return len(products)
        except InvalidTokenError as e:
            logger.warning(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
