"""empty message

Revision ID: 93d7162e6efb
Revises: c48f006e91f9
Create Date: 2022-08-08 22:34:55.252734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d7162e6efb'
down_revision = 'c48f006e91f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product_data', 'out_of_stock',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.add_column('users', sa.Column('email_activated', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'email_activated')
    op.alter_column('product_data', 'out_of_stock',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
