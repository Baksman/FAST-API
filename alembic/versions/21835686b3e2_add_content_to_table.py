"""add content to table

Revision ID: 21835686b3e2
Revises: fe0f51c515ff
Create Date: 2022-11-03 07:07:16.563658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21835686b3e2'
down_revision = 'fe0f51c515ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.createtable('users', sa.Column('id', sa.Integer(), nullable=False), a.Column(
        'email', sa.String(), nullable=False),
        sa.Column('password', sa.String(),nullable=False),
        sa.Column('created_at',  sa.TIMESTAMP(timezone=True), nullable=False,server_default=sa.Text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users',)
