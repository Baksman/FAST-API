"""create post table

Revision ID: fe0f51c515ff
Revises: 
Create Date: 2022-11-03 06:51:55.950645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe0f51c515ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True,server_default='True'),
                    sa.Column('content', sa.String(), nullable=False))

    
def downgrade() -> None:
    op.drop_table('posts')
    pass
