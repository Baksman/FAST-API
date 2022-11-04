"""fix(user table not added)

Revision ID: 520265d9be33
Revises: b0d77a9ed870
Create Date: 2022-11-03 08:50:42.858929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '520265d9be33'
down_revision = 'b0d77a9ed870'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column(
        'email', sa.String(), nullable=False),
        sa.Column('password', sa.String(),nullable=False),
        sa.Column('created_at',  sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users',)
