from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.db.models import OrderOrm, ProductAndOrderOrm
from src.data.logoscoffee.exceptions import UnknownError, DatabaseError
from src.data.logoscoffee.session_manager import SessionManager

async def create_draft_orm(s: AsyncSession, client_id: int) -> OrderOrm:
    order_orm = OrderOrm(client_id = client_id)
    s.add(order_orm)
    await s.flush()
    return order_orm
