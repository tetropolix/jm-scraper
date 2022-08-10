"""empty message

Revision ID: e223aba13111
Revises: 0fc563b8c303
Create Date: 2022-08-10 12:05:31.626441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e223aba13111'
down_revision = '0fc563b8c303'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.drop_column('profiles', 'user_id')
    # ### end Alembic commands ###
