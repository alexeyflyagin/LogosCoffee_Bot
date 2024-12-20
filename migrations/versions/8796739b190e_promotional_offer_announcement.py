"""promotional_offer -> announcement

Revision ID: 8796739b190e
Revises: 50f93cb4476f
Create Date: 2024-11-19 14:57:49.464975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8796739b190e'
down_revision: Union[str, None] = '50f93cb4476f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcement',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_create', sa.DateTime(), nullable=False),
    sa.Column('date_last_distribute', sa.DateTime(), nullable=True),
    sa.Column('text_content', sa.String(), nullable=True),
    sa.Column('preview_photo', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('promotional_offer')
    op.add_column('admin_account', sa.Column('date_last_announcement_distributing', sa.DateTime(), nullable=True))
    op.drop_column('admin_account', 'date_last_offer_distributing')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_account', sa.Column('date_last_offer_distributing', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('admin_account', 'date_last_announcement_distributing')
    op.create_table('promotional_offer',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date_create', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('date_last_distribute', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('text_content', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('preview_photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='promotional_offer_pkey')
    )
    op.drop_table('announcement')
    # ### end Alembic commands ###
