"""empty message

Revision ID: eb6da4113767
Revises: bb0f7a1cd900
Create Date: 2021-06-27 13:17:49.281728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb6da4113767'
down_revision = 'bb0f7a1cd900'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('start_time', sa.VARCHAR(length=16), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'start_time')
    # ### end Alembic commands ###