"""empty message

Revision ID: 0857f9eeb786
Revises: 75e4262a0ca5
Create Date: 2020-12-23 01:00:19.958303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0857f9eeb786'
down_revision = '75e4262a0ca5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'image_link',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('artists', 'image_link',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###