from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.logoscoffee.dao.units import set_with_for_update_if
from src.data.logoscoffee.db.models import EmployeeAccountOrm


async def get_by_id(
        s: AsyncSession,
        _id: int,
        with_for_update: bool = False
) -> EmployeeAccountOrm | None:
    query = select(EmployeeAccountOrm).filter(EmployeeAccountOrm.id == _id)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def get_by_key(
        s: AsyncSession,
        key: str,
        with_for_update: bool = False
) -> EmployeeAccountOrm | None:
    query = select(EmployeeAccountOrm).filter(EmployeeAccountOrm.key == key)
    query = set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()
