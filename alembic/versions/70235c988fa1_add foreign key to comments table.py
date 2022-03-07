"""add foreign key to comments table

Revision ID: 70235c988fa1
Revises: e0f0fc721ada
Create Date: 2022-03-06 19:30:19.728955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70235c988fa1'
down_revision = 'e0f0fc721ada'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("comments", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("comments_users_fk", source_table="comments", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("comments_users_fk", table_name="comments")
    op.drop_column("posts", "owner_id")
    pass
