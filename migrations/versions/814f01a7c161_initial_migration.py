"""initial migration

Revision ID: 814f01a7c161
Revises: 7bdb18ba5b00
Create Date: 2024-07-11 11:07:10.382775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '814f01a7c161'
down_revision: Union[str, None] = '7bdb18ba5b00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_rw_transport', schema=None) as batch_op:
        batch_op.add_column(sa.Column('container_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'containers', ['container_id'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_rw_transport', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('container_id')

    # ### end Alembic commands ###
