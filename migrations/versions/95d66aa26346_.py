"""empty message

Revision ID: 95d66aa26346
Revises: e223aba13111
Create Date: 2022-08-16 11:17:57.979818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95d66aa26346'
down_revision = 'e223aba13111'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('predefined_profile_filters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('max_price', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('min_price', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('percent_off', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters_brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predefined_profile_filters', sa.Integer(), nullable=True),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
    sa.ForeignKeyConstraint(['predefined_profile_filters'], ['predefined_profile_filters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters_eshop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predefined_profile_filters', sa.Integer(), nullable=True),
    sa.Column('eshop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['eshop_id'], ['eshops.id'], ),
    sa.ForeignKeyConstraint(['predefined_profile_filters'], ['predefined_profile_filters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters_gender',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predefined_profile_filters', sa.Integer(), nullable=True),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], ),
    sa.ForeignKeyConstraint(['predefined_profile_filters'], ['predefined_profile_filters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters_shoe_size_cm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predefined_profile_filters', sa.Integer(), nullable=True),
    sa.Column('shoe_size_cm_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['predefined_profile_filters'], ['predefined_profile_filters.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_cm_id'], ['shoe_sizes_cm.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters_shoe_size_eu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predefined_profile_filters', sa.Integer(), nullable=True),
    sa.Column('shoe_size_eu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['predefined_profile_filters'], ['predefined_profile_filters.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_eu_id'], ['shoe_sizes_eu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters_shoe_size_uk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predefined_profile_filters', sa.Integer(), nullable=True),
    sa.Column('shoe_size_uk_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['predefined_profile_filters'], ['predefined_profile_filters.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_uk_id'], ['shoe_sizes_uk.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters_shoe_size_us',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('predefined_profile_filters', sa.Integer(), nullable=True),
    sa.Column('shoe_size_us_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['predefined_profile_filters'], ['predefined_profile_filters.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_us_id'], ['shoe_sizes_us.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('profiles', sa.Column('gender_id', sa.Integer(), nullable=True))
    op.add_column('profiles', sa.Column('send_notifications', sa.Boolean(), nullable=False))
    op.alter_column('profiles', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'profiles', 'genders', ['gender_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.alter_column('profiles', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('profiles', 'send_notifications')
    op.drop_column('profiles', 'gender_id')
    op.drop_table('predefined_profile_filters_shoe_size_us')
    op.drop_table('predefined_profile_filters_shoe_size_uk')
    op.drop_table('predefined_profile_filters_shoe_size_eu')
    op.drop_table('predefined_profile_filters_shoe_size_cm')
    op.drop_table('predefined_profile_filters_gender')
    op.drop_table('predefined_profile_filters_eshop')
    op.drop_table('predefined_profile_filters_brand')
    op.drop_table('predefined_profile_filters')
    # ### end Alembic commands ###
