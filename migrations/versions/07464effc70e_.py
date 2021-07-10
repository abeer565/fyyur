"""empty message

Revision ID: 07464effc70e
Revises: 043a30762e38
Create Date: 2021-06-29 22:09:06.206676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07464effc70e'
down_revision = '043a30762e38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'looking_for_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'looking_for_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###