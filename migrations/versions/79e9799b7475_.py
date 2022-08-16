"""empty message

Revision ID: 79e9799b7475
Revises: 95d66aa26346
Create Date: 2022-08-16 11:21:42.550149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79e9799b7475'
down_revision = '95d66aa26346'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('eshops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=128), nullable=False),
    sa.Column('eshop_logo_url', sa.String(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('domain')
    )
    op.create_table('genders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gender')
    )
    op.create_table('shoe_sizes_cm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('shoe_sizes_eu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('shoe_sizes_uk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('shoe_sizes_us',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('email_activated', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('shoe_id', sa.String(length=64), nullable=False),
    sa.Column('product_image_url', sa.String(length=512), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shoe_id')
    )
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('avatar_uri', sa.String(length=256), nullable=True),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('send_notifications', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('predefined_profile_filters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('max_price', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('min_price', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('percent_off', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scraped_at', sa.DateTime(), nullable=False),
    sa.Column('product_url', sa.String(length=512), nullable=False),
    sa.Column('final_price', sa.Numeric(precision=6, scale=2), nullable=False),
    sa.Column('original_price', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('percent_off', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('out_of_stock', sa.Boolean(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('eshop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['eshop_id'], ['eshops.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_gender',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile_gender',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile_product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
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
    op.create_table('shoe_size_cm_product_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shoe_size_id', sa.Integer(), nullable=True),
    sa.Column('product_data_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_data_id'], ['product_data.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_id'], ['shoe_sizes_cm.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shoe_size_eu_product_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shoe_size_id', sa.Integer(), nullable=True),
    sa.Column('product_data_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_data_id'], ['product_data.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_id'], ['shoe_sizes_eu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shoe_size_uk_product_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shoe_size_id', sa.Integer(), nullable=True),
    sa.Column('product_data_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_data_id'], ['product_data.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_id'], ['shoe_sizes_uk.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shoe_size_us_product_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shoe_size_id', sa.Integer(), nullable=True),
    sa.Column('product_data_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_data_id'], ['product_data.id'], ),
    sa.ForeignKeyConstraint(['shoe_size_id'], ['shoe_sizes_us.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shoe_size_us_product_data')
    op.drop_table('shoe_size_uk_product_data')
    op.drop_table('shoe_size_eu_product_data')
    op.drop_table('shoe_size_cm_product_data')
    op.drop_table('predefined_profile_filters_shoe_size_us')
    op.drop_table('predefined_profile_filters_shoe_size_uk')
    op.drop_table('predefined_profile_filters_shoe_size_eu')
    op.drop_table('predefined_profile_filters_shoe_size_cm')
    op.drop_table('predefined_profile_filters_gender')
    op.drop_table('predefined_profile_filters_eshop')
    op.drop_table('predefined_profile_filters_brand')
    op.drop_table('profile_product')
    op.drop_table('profile_gender')
    op.drop_table('product_gender')
    op.drop_table('product_data')
    op.drop_table('predefined_profile_filters')
    op.drop_table('profiles')
    op.drop_table('products')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('shoe_sizes_us')
    op.drop_table('shoe_sizes_uk')
    op.drop_table('shoe_sizes_eu')
    op.drop_table('shoe_sizes_cm')
    op.drop_table('genders')
    op.drop_table('eshops')
    op.drop_table('brands')
    # ### end Alembic commands ###
