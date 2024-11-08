"""added: employee_account

Revision ID: 0fe70f86cc11
Revises: 22d97c7af9ce
Create Date: 2024-11-03 15:23:37.602269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import insert
from sqlalchemy.dialects import mysql

from src import config
from src.data.logoscoffee.db.models import EmployeeAccountOrm

# revision identifiers, used by Alembic.
revision: str = '0fe70f86cc11'
down_revision: Union[str, None] = '22d97c7af9ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee_account',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('token', mysql.VARCHAR(length=8), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.execute(
        insert(EmployeeAccountOrm).values(token=config.DEFAULT_EMPLOYEE_TOKEN_FOR_LOGIN)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee_account')
    # ### end Alembic commands ###
