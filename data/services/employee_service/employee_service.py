from loguru import logger

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typeguard import typechecked

from data.services.database import database
from data.services.exceptions import *
from data.services.models import EmployeeAccountOrm

@typechecked
async def log_in(token: str):
    try:
        async with database.session_factory() as s:
            query = await s.execute(select(EmployeeAccountOrm).filter(EmployeeAccountOrm.token == token))
            account = query.scalars().first()
            if account is None:
                raise InvalidToken(token)
    except InvalidToken as e:
        logger.warning(e)
        raise
    except SQLAlchemyError as e:
        logger.error(e)
        raise DatabaseError(e)
    except Exception as e:
        logger.exception(e)
        raise UnknownError(e)
