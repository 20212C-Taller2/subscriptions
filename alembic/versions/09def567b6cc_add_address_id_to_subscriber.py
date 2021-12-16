"""Add address id to subscriber

Revision ID: 09def567b6cc
Revises: 2e96aac4a409
Create Date: 2021-12-15 21:35:57.851806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09def567b6cc'
down_revision = '2e96aac4a409'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriber', sa.Column('address', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscriber', 'address')
    # ### end Alembic commands ###
