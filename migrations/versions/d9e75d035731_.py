"""empty message

Revision ID: d9e75d035731
Revises: 4147613a9092
Create Date: 2022-09-04 09:58:01.910024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9e75d035731'
down_revision = '4147613a9092'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scrapes', sa.Column('products_count', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scrapes', 'products_count')
    # ### end Alembic commands ###
