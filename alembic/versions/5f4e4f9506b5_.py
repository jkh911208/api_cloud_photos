"""empty message

Revision ID: 5f4e4f9506b5
Revises: 1c3f4895ed4d
Create Date: 2021-05-15 22:03:28.147734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f4e4f9506b5'
down_revision = '1c3f4895ed4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('thumbnail', sa.String(), nullable=False))
    op.add_column('photos', sa.Column('resize', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photos', 'resize')
    op.drop_column('photos', 'thumbnail')
    # ### end Alembic commands ###