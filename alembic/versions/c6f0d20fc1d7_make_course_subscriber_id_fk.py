"""make course subscriber id fk

Revision ID: c6f0d20fc1d7
Revises: 09def567b6cc
Create Date: 2021-12-18 19:01:07.549755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6f0d20fc1d7'
down_revision = '09def567b6cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'course', 'subscriber', ['owner_id'], ['subscriber_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'course', type_='foreignkey')
    # ### end Alembic commands ###