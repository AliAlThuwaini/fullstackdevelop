"""empty message

Revision ID: 1063691d2982
Revises: 3c47e7865cdd
Create Date: 2020-12-22 23:53:17.619602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1063691d2982'
down_revision = '3c47e7865cdd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_description', sa.String(), nullable=True))
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'seeking_venue')
    op.drop_column('artists', 'seeking_description')
    # ### end Alembic commands ###
