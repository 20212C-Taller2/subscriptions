"""Subscriptions

Revision ID: deecdbe7efc1
Revises: 
Create Date: 2021-11-25 18:29:52.969211

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import table, column, String

revision = 'deecdbe7efc1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription',
                    sa.Column('code', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('code')
                    )
    op.create_index(op.f('ix_subscription_code'), 'subscription', ['code'], unique=True)

    # ### end Alembic commands ###
    sub_table = table('subscription',
                      column('code', String),
                      column('description', String),
                      )
    op.bulk_insert(sub_table, [
        {"code": "FREE", "description": "Free Subscription"},
        {"code": "BASIC", "description": "Basic Subscription"},
        {"code": "FULL", "description": "Full Subscription"},
    ])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscription_code'), table_name='subscription')
    op.drop_table('subscription')
    # ### end Alembic commands ###
