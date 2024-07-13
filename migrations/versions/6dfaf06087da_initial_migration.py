"""initial migration

Revision ID: 6dfaf06087da
Revises: 9169da0f8874
Create Date: 2024-07-11 10:49:03.643079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dfaf06087da'
down_revision: Union[str, None] = '9169da0f8874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_rw_transport', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weight', sa.Numeric(precision=15, scale=4), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_rw_transport', schema=None) as batch_op:
        batch_op.drop_column('weight')

    # ### end Alembic commands ###