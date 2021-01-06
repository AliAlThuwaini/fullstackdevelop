"""empty message

Revision ID: 75e4262a0ca5
Revises: 38a32e7a8de1
Create Date: 2020-12-23 00:58:44.521610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75e4262a0ca5'
down_revision = '38a32e7a8de1'
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
    op.add_column('shows', sa.Column('artist_image_link', sa.Integer(), nullable=False))
    op.add_column('shows', sa.Column('artist_name', sa.Integer(), nullable=False))
    op.add_column('shows', sa.Column('venue_name', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'shows', 'artists', ['artist_image_link'], ['image_link'])
    op.create_foreign_key(None, 'shows', 'artists', ['artist_name'], ['name'])
    op.create_foreign_key(None, 'shows', 'venues', ['venue_name'], ['name'])
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_column('shows', 'venue_name')
    op.drop_column('shows', 'artist_name')
    op.drop_column('shows', 'artist_image_link')
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('artists', 'image_link',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
