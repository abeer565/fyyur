"""empty message

Revision ID: 25b753d88f3c
Revises: 9006332285d2
Create Date: 2021-07-04 13:18:08.464593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25b753d88f3c'
down_revision = '9006332285d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'seeking_talent',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'seeking_talent',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###
