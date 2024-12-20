"""added: product, order

Revision ID: 50f93cb4476f
Revises: 6c02730af63c
Create Date: 2024-11-16 14:20:35.764269

"""
from decimal import Decimal
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.data.logoscoffee.db.models import ProductOrm

# revision identifiers, used by Alembic.
revision: str = '50f93cb4476f'
down_revision: Union[str, None] = '6c02730af63c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_create', sa.DateTime(), nullable=False),
                    sa.Column('is_available', sa.Boolean(), nullable=False),
                    sa.Column('price', sa.DECIMAL(), nullable=False),
                    sa.Column('product_name', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('preview_photo', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('order',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_create', sa.DateTime(), nullable=False),
                    sa.Column('client_id', sa.BIGINT(), nullable=False),
                    sa.Column('pickup_code', sa.VARCHAR(length=4), nullable=True),
                    sa.Column('date_pending', sa.DateTime(), nullable=True),
                    sa.Column('date_cooking', sa.DateTime(), nullable=True),
                    sa.Column('date_ready', sa.DateTime(), nullable=True),
                    sa.Column('date_completed', sa.DateTime(), nullable=True),
                    sa.Column('date_canceled', sa.DateTime(), nullable=True),
                    sa.Column('cancel_details', sa.String(), nullable=True),
                    sa.Column('details', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['client_id'], ['client_account.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('product_and_order',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_create', sa.DateTime(), nullable=False),
                    sa.Column('order_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('product_price', sa.DECIMAL(), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.add_column('event_subscriber', sa.Column('data', sa.JSON(), nullable=True))

    op.execute(sa.insert(ProductOrm).values(
        is_available=True,
        price=Decimal('150'),
        product_name="Капучино",
        description="Классический итальянский напиток на основе эспрессо и вспененного молока. Идеальное сочетание насыщенного кофе с нежной молочной пенкой.",
    ))
    op.execute(sa.insert(ProductOrm).values(
        is_available=True,
        price=Decimal('100'),
        product_name="Американо",
        description="Легкий, мягкий черный кофе, приготовленный из эспрессо и горячей воды. Прекрасный выбор для тех, кто ценит чистый вкус зерен без лишних добавок.",
    ))
    op.execute(sa.insert(ProductOrm).values(
        is_available=True,
        price=Decimal('300'),
        product_name="Латте с карамелью",
        description="Восхитительный латте с добавлением карамельного сиропа. Кремовая текстура молока и сладкая нотка карамели делают этот напиток настоящим удовольствием.",
    ))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event_subscriber', 'data')
    op.drop_table('product_and_order')
    op.drop_table('order')
    op.drop_table('product')
    # ### end Alembic commands ###
