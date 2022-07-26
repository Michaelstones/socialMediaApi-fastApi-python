"""add column to post table

Revision ID: a4f445a375a5
Revises: cf179cf9c97e
Create Date: 2022-07-26 13:00:08.790412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4f445a375a5'
down_revision = 'cf179cf9c97e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
