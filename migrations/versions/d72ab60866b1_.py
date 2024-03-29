"""empty message

Revision ID: d72ab60866b1
Revises: be6f4f957c04
Create Date: 2022-08-29 12:06:29.102657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72ab60866b1'
down_revision = 'be6f4f957c04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email_activated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email_activated', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
