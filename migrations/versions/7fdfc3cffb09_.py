"""empty message

Revision ID: 7fdfc3cffb09
Revises: d9e75d035731
Create Date: 2022-09-04 10:17:30.843981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fdfc3cffb09'
down_revision = 'd9e75d035731'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scrapes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scraped_at', sa.DateTime(), nullable=False),
    sa.Column('products_scraped', sa.Integer(), nullable=False),
    sa.Column('product_data_scraped', sa.Integer(), nullable=False),
    sa.Column('scrape_length_secs', sa.Numeric(precision=8, scale=2), nullable=False),
    sa.Column('products_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scrapes')
    # ### end Alembic commands ###
