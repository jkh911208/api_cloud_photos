"""empty message

Revision ID: d53afe4c4f56
Revises: 
Create Date: 2021-05-21 19:28:32.795073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd53afe4c4f56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('photos',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created', sa.BigInteger(), nullable=False),
    sa.Column('original_filename', sa.String(), nullable=False),
    sa.Column('original_datetime', sa.BigInteger(), nullable=False),
    sa.Column('original_make', sa.String(), nullable=True),
    sa.Column('original_model', sa.String(), nullable=True),
    sa.Column('original_width', sa.Integer(), nullable=False),
    sa.Column('original_height', sa.Integer(), nullable=False),
    sa.Column('new_filename', sa.String(), nullable=False),
    sa.Column('thumbnail', sa.String(), nullable=False),
    sa.Column('resize', sa.String(), nullable=False),
    sa.Column('md5', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('owner', sa.String(length=36), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['owner'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('owner', 'md5')
    )
    op.create_index(op.f('ix_photos_id'), 'photos', ['id'], unique=True)
    op.create_index(op.f('ix_photos_original_datetime'), 'photos', ['original_datetime'], unique=False)
    op.create_index(op.f('ix_photos_owner'), 'photos', ['owner'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_photos_owner'), table_name='photos')
    op.drop_index(op.f('ix_photos_original_datetime'), table_name='photos')
    op.drop_index(op.f('ix_photos_id'), table_name='photos')
    op.drop_table('photos')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
