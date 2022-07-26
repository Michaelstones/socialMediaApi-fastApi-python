"""add foreign_key to posts

Revision ID: 7c06e564e332
Revises: a4f445a375a5
Create Date: 2022-07-26 13:58:05.442114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c06e564e332'
down_revision = 'a4f445a375a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE' )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_key_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
