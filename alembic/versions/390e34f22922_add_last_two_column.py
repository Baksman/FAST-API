"""add last two column

Revision ID: 390e34f22922
Revises: eb9a182b881f
Create Date: 2022-11-03 13:00:24.678745

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '390e34f22922'
down_revision = 'eb9a182b881f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column('posts',
    #                 sa.Column('is_published', sa.Boolean, server_default='TRUE',nullable=False))
    op.add_column('posts',
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),nullable=False))


def downgrade() -> None:
    op.drop_column('posts','is_published')
    op.drop_column('posts','created_at')
    pass
