"""initial migration

Revision ID: 80aeed2823ee
Revises: 1514183349df
Create Date: 2024-07-09 16:54:39.916509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80aeed2823ee'
down_revision: Union[str, None] = '1514183349df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_rw_route',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('weight', sa.Numeric(precision=15, scale=4), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('sum', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('comment', sa.String(length=300), nullable=True),
    sa.Column('orderrw_id', sa.Integer(), nullable=False),
    sa.Column('station_otpr_id', sa.Integer(), nullable=False),
    sa.Column('station_nazn_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['orderrw_id'], ['order_rw.id'], ),
    sa.ForeignKeyConstraint(['station_nazn_id'], ['stations.id'], ),
    sa.ForeignKeyConstraint(['station_otpr_id'], ['stations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('order_rw_route', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_order_rw_route_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_rw_route', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_order_rw_route_id'))

    op.drop_table('order_rw_route')
    # ### end Alembic commands ###