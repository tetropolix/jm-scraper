"""empty message

Revision ID: a0080cbbd2ec
Revises: 0543cd574f26
Create Date: 2022-08-29 11:58:42.179741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0080cbbd2ec'
down_revision = '0543cd574f26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('confirmed_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed_on')
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
