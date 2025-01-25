from datetime import datetime

from src.loggers import service_logger as logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.checks import check_text_is_not_empty
from src.data.logoscoffee.dao import dao_order
from src.data.logoscoffee.db.models import OrderOrm, ClientAccountOrm
from src.data.logoscoffee.exceptions import UnknownError, InvalidTokenError, EmptyTextError, \
    OtherOrderIsPlacedAlreadyError, DatabaseError
from src.data.logoscoffee.interfaces.client_order_service import ClientOrderService
from src.data.logoscoffee.models import PlaceOrderData
from src.data.logoscoffee.services.utils import get_client_account_by_token
from src.data.logoscoffee.session_manager import SessionManager


class ClientOrderServiceImpl(ClientOrderService):

    def __init__(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    async def __can_place_order(self, s: AsyncSession, account: ClientAccountOrm):
        order = await dao_order.get_active_order_by_client_id(s, client_id=account.id)
        if order is not None:
            raise OtherOrderIsPlacedAlreadyError(id=order.id)

    async def can_place_order(self, token: str):
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                await self.__can_place_order(s, account)
        except (InvalidTokenError, OtherOrderIsPlacedAlreadyError) as e:
            logger.debug(e)
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
            data: PlaceOrderData,
    ):
        try:
            async with self.__session_manager.get_session() as s:
                account = await get_client_account_by_token(s, token)
                await self.__can_place_order(s, account)
                check_text_is_not_empty(data.details)
                new_order = OrderOrm(client_id=account.id, date_pending=datetime.now(), details=data.details)

                s.add(new_order)
                await s.commit()
        except (InvalidTokenError, EmptyTextError, OtherOrderIsPlacedAlreadyError) as e:
            logger.debug(e)
            raise
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseError(e)
        except Exception as e:
            logger.exception(e)
            raise UnknownError(e)
