"""empty message

Revision ID: c92f8861c5da
Revises: 4c81272f3258
Create Date: 2021-07-08 13:21:06.520220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c92f8861c5da'
down_revision = '4c81272f3258'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###
