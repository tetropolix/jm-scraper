"""empty message

Revision ID: 1497d5c778de
Revises: 22df5a7960c7
Create Date: 2022-09-02 10:30:29.034730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1497d5c778de'
down_revision = '22df5a7960c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_data_product_id_fkey', 'product_data', type_='foreignkey')
    op.create_foreign_key(None, 'product_data', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_data', type_='foreignkey')
    op.create_foreign_key('product_data_product_id_fkey', 'product_data', 'products', ['product_id'], ['id'])
    # ### end Alembic commands ###
