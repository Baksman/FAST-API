"""add foreign key to post table

Revision ID: eb9a182b881f
Revises: 520265d9be33
Create Date: 2022-11-03 09:14:16.511903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb9a182b881f'
down_revision = '520265d9be33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False),)
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=['user_id'],remote_cols=['id'],ondelete='CASCADE'),



def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column("posts","user_id")
