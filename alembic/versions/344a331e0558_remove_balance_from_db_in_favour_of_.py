"""remove balance from db in favour of wallet get balance

Revision ID: 344a331e0558
Revises: 6ad2c9e10a1a
Create Date: 2021-12-19 11:04:57.281458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '344a331e0558'
down_revision = '6ad2c9e10a1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscriber', 'balance')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriber', sa.Column('balance', sa.NUMERIC(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
