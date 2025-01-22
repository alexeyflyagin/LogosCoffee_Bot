"""added menu table

Revision ID: b567e15e9bd2
Revises: 9a2df568e37c
Create Date: 2025-01-22 21:55:32.880841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import insert

from src.data.logoscoffee.db.models import MenuOrm
from src.presentation.resources import strings

# revision identifiers, used by Alembic.
revision: str = 'b567e15e9bd2'
down_revision: Union[str, None] = '9a2df568e37c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('last_date_update', sa.DateTime(), nullable=False),
    sa.Column('text_content', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.execute(insert(MenuOrm))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu')
    # ### end Alembic commands ###
