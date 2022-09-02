"""empty message

Revision ID: bf9e9bac7f40
Revises: ba10fb19f911
Create Date: 2022-08-24 21:08:05.725982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf9e9bac7f40'
down_revision = 'ba10fb19f911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'authenticated',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'authenticated',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###